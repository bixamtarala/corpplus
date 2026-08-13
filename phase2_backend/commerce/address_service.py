"""Ownership-safe address persistence and default-address management."""

from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from .address_schemas import AddressCreateBody, AddressUpdateBody
from .auth_service import InvalidPhone, normalize_indian_phone
from .models import Address, AuditEvent, CommerceUser


class AddressNotFound(LookupError):
    pass


class AddressService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, user_id: str) -> list[Address]:
        return list(
            self.db.scalars(
                select(Address)
                .where(Address.user_id == user_id, Address.is_active.is_(True))
                .order_by(Address.is_default.desc(), Address.created_at, Address.id)
            )
        )

    def create(self, user_id: str, payload: AddressCreateBody) -> Address:
        self._lock_user(user_id)
        phone = normalize_indian_phone(payload.recipient_phone)
        has_active_address = self.db.scalar(
            select(Address.id).where(Address.user_id == user_id, Address.is_active.is_(True)).limit(1)
        )
        make_default = payload.make_default or has_active_address is None
        if make_default:
            self._clear_defaults(user_id)
        values = payload.model_dump(exclude={"recipient_phone", "make_default"})
        address = Address(
            user_id=user_id,
            recipient_phone_e164=phone,
            is_default=make_default,
            **values,
        )
        self.db.add(address)
        self.db.flush()
        self._audit(user_id, address.id, "address.created")
        self.db.commit()
        self.db.refresh(address)
        return address

    def update(self, user_id: str, address_id: str, payload: AddressUpdateBody) -> Address:
        self._lock_user(user_id)
        address = self._owned_active(user_id, address_id, lock=True)
        changes = payload.model_dump(exclude_unset=True)
        make_default = changes.pop("make_default", None)
        if "recipient_phone" in changes:
            changes["recipient_phone_e164"] = normalize_indian_phone(changes.pop("recipient_phone"))
        for field, value in changes.items():
            setattr(address, field, value)
        if make_default is True and not address.is_default:
            self._clear_defaults(user_id)
            address.is_default = True
        self._audit(user_id, address.id, "address.updated")
        self.db.commit()
        self.db.refresh(address)
        return address

    def delete(self, user_id: str, address_id: str) -> None:
        self._lock_user(user_id)
        address = self._owned_active(user_id, address_id, lock=True)
        was_default = address.is_default
        address.is_active = False
        address.is_default = False
        if was_default:
            replacement = self.db.scalar(
                select(Address)
                .where(
                    Address.user_id == user_id,
                    Address.is_active.is_(True),
                    Address.id != address.id,
                )
                .order_by(Address.created_at, Address.id)
                .limit(1)
                .with_for_update()
            )
            if replacement is not None:
                replacement.is_default = True
        self._audit(user_id, address.id, "address.deleted")
        self.db.commit()

    def set_default(self, user_id: str, address_id: str) -> Address:
        self._lock_user(user_id)
        address = self._owned_active(user_id, address_id, lock=True)
        if not address.is_default:
            self._clear_defaults(user_id)
            address.is_default = True
            self._audit(user_id, address.id, "address.default_set")
            self.db.commit()
            self.db.refresh(address)
        return address

    def _owned_active(self, user_id: str, address_id: str, *, lock: bool) -> Address:
        statement = select(Address).where(
            Address.id == address_id,
            Address.user_id == user_id,
            Address.is_active.is_(True),
        )
        if lock:
            statement = statement.with_for_update()
        address = self.db.scalar(statement)
        if address is None:
            raise AddressNotFound("Address not found")
        return address

    def _clear_defaults(self, user_id: str) -> None:
        self.db.execute(
            update(Address)
            .where(Address.user_id == user_id, Address.is_active.is_(True), Address.is_default.is_(True))
            .values(is_default=False)
        )

    def _lock_user(self, user_id: str) -> None:
        # Serializes concurrent default-address changes on PostgreSQL. SQLite
        # ignores FOR UPDATE but remains covered by service tests.
        self.db.scalar(select(CommerceUser.id).where(CommerceUser.id == user_id).with_for_update())

    def _audit(self, user_id: str, address_id: str, action: str) -> None:
        self.db.add(
            AuditEvent(
                actor_user_id=user_id,
                entity_type="address",
                entity_id=address_id,
                action=action,
                payload={},
            )
        )


__all__ = ["AddressNotFound", "AddressService", "InvalidPhone"]
