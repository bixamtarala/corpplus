import 'dart:convert';

class CommerceCategory {
  const CommerceCategory({
    required this.id,
    required this.slug,
    required this.name,
  });
  final String id;
  final String slug;
  final String name;

  factory CommerceCategory.fromJson(Map<String, dynamic> json) =>
      CommerceCategory(
        id: json['id'] as String? ?? '',
        slug: json['slug'] as String? ?? '',
        name: json['name'] as String? ?? '',
      );
}

class CommerceSku {
  const CommerceSku({
    required this.id,
    required this.code,
    required this.packQuantity,
    required this.unitOfMeasure,
    required this.minimumOrderQuantity,
    required this.quantityStep,
    this.grade,
    this.originDistrict,
    this.originState,
    this.pricePaise,
    this.currency = 'INR',
  });
  final String id;
  final String code;
  final double packQuantity;
  final String unitOfMeasure;
  final double minimumOrderQuantity;
  final double quantityStep;
  final String? grade;
  final String? originDistrict;
  final String? originState;
  final int? pricePaise;
  final String currency;

  factory CommerceSku.fromJson(Map<String, dynamic> json) {
    final price = json['price'] as Map<String, dynamic>?;
    return CommerceSku(
      id: json['id'] as String? ?? '',
      code: json['code'] as String? ?? '',
      packQuantity: _double(json['pack_quantity']),
      unitOfMeasure: json['unit_of_measure'] as String? ?? '',
      minimumOrderQuantity: _double(json['minimum_order_quantity']),
      quantityStep: _double(json['quantity_step']),
      grade: json['grade'] as String?,
      originDistrict: json['origin_district'] as String?,
      originState: json['origin_state'] as String?,
      pricePaise: (price?['amount_paise'] as num?)?.toInt(),
      currency: price?['currency'] as String? ?? 'INR',
    );
  }

  String get packLabel => '${_compact(packQuantity)} $unitOfMeasure';
}

class CommerceProduct {
  const CommerceProduct({
    required this.id,
    required this.slug,
    required this.name,
    required this.category,
    required this.skus,
    this.description,
    this.storageGuidance,
    this.sourceOrganizationName,
  });
  final String id;
  final String slug;
  final String name;
  final CommerceCategory category;
  final List<CommerceSku> skus;
  final String? description;
  final String? storageGuidance;
  final String? sourceOrganizationName;

  factory CommerceProduct.fromJson(Map<String, dynamic> json) =>
      CommerceProduct(
        id: json['id'] as String? ?? '',
        slug: json['slug'] as String? ?? '',
        name: json['name'] as String? ?? '',
        category: CommerceCategory.fromJson(
          json['category'] as Map<String, dynamic>,
        ),
        skus: (json['skus'] as List<dynamic>? ?? const [])
            .map((item) => CommerceSku.fromJson(item as Map<String, dynamic>))
            .toList(growable: false),
        description: json['description'] as String?,
        storageGuidance: json['storage_guidance'] as String?,
        sourceOrganizationName: json['source_organization_name'] as String?,
      );
}

class ServiceabilityDecision {
  const ServiceabilityDecision({
    required this.pincode,
    required this.serviceable,
    required this.status,
    required this.reason,
  });
  final String pincode;
  final bool serviceable;
  final String status;
  final String reason;
  factory ServiceabilityDecision.fromJson(Map<String, dynamic> json) =>
      ServiceabilityDecision(
        pincode: json['pincode'] as String? ?? '',
        serviceable: json['serviceable'] as bool? ?? false,
        status: json['status'] as String? ?? 'not_serviceable',
        reason: json['reason'] as String? ?? '',
      );
}

class CommerceAddress {
  const CommerceAddress({
    required this.id,
    required this.label,
    required this.recipientName,
    required this.recipientPhone,
    required this.line1,
    required this.locality,
    required this.district,
    required this.state,
    required this.pincode,
    required this.isDefault,
    required this.serviceability,
    this.line2,
    this.landmark,
  });
  final String id;
  final String label;
  final String recipientName;
  final String recipientPhone;
  final String line1;
  final String? line2;
  final String? landmark;
  final String locality;
  final String district;
  final String state;
  final String pincode;
  final bool isDefault;
  final ServiceabilityDecision serviceability;
  factory CommerceAddress.fromJson(Map<String, dynamic> json) =>
      CommerceAddress(
        id: json['id'] as String? ?? '',
        label: json['label'] as String? ?? '',
        recipientName: json['recipient_name'] as String? ?? '',
        recipientPhone: json['recipient_phone'] as String? ?? '',
        line1: json['line1'] as String? ?? '',
        line2: json['line2'] as String?,
        landmark: json['landmark'] as String?,
        locality: json['locality'] as String? ?? '',
        district: json['district'] as String? ?? '',
        state: json['state'] as String? ?? '',
        pincode: json['pincode'] as String? ?? '',
        isDefault: json['is_default'] as bool? ?? false,
        serviceability: ServiceabilityDecision.fromJson(
          json['serviceability'] as Map<String, dynamic>,
        ),
      );
}

class CartIssue {
  const CartIssue({
    required this.code,
    required this.message,
    required this.severity,
  });
  final String code;
  final String message;
  final String severity;
  factory CartIssue.fromJson(Map<String, dynamic> json) => CartIssue(
    code: json['code'] as String? ?? '',
    message: json['message'] as String? ?? '',
    severity: json['severity'] as String? ?? 'error',
  );
}

class CommerceCartItem {
  const CommerceCartItem({
    required this.id,
    required this.skuId,
    required this.skuCode,
    required this.productName,
    required this.quantity,
    required this.unitOfMeasure,
    required this.minimumOrderQuantity,
    required this.quantityStep,
    required this.issues,
    this.unitPricePaise,
    this.lineTotalPaise,
    this.availableQuantity,
  });
  final String id;
  final String skuId;
  final String skuCode;
  final String productName;
  final double quantity;
  final String unitOfMeasure;
  final double minimumOrderQuantity;
  final double quantityStep;
  final int? unitPricePaise;
  final int? lineTotalPaise;
  final double? availableQuantity;
  final List<CartIssue> issues;
  factory CommerceCartItem.fromJson(Map<String, dynamic> json) =>
      CommerceCartItem(
        id: json['id'] as String? ?? '',
        skuId: json['sku_id'] as String? ?? '',
        skuCode: json['sku_code'] as String? ?? '',
        productName: json['product_name'] as String? ?? '',
        quantity: _double(json['quantity']),
        unitOfMeasure: json['unit_of_measure'] as String? ?? '',
        minimumOrderQuantity: _double(json['minimum_order_quantity']),
        quantityStep: _double(json['quantity_step']),
        unitPricePaise: (json['unit_price_paise'] as num?)?.toInt(),
        lineTotalPaise: (json['line_total_paise'] as num?)?.toInt(),
        availableQuantity: json['available_quantity'] == null
            ? null
            : _double(json['available_quantity']),
        issues: (json['issues'] as List<dynamic>? ?? const [])
            .map((item) => CartIssue.fromJson(item as Map<String, dynamic>))
            .toList(growable: false),
      );
}

class CommerceCart {
  const CommerceCart({
    required this.id,
    required this.ownerType,
    required this.version,
    required this.currency,
    required this.subtotalPaise,
    required this.itemCount,
    required this.validForCheckout,
    required this.validationStatus,
    required this.issues,
    required this.items,
    this.guestToken,
    this.addressId,
    this.deliveryPincode,
    this.deliveryFeePaise,
    this.totalPaise,
  });
  final String id;
  final String ownerType;
  final String? guestToken;
  final int version;
  final String currency;
  final String? addressId;
  final String? deliveryPincode;
  final int subtotalPaise;
  final int? deliveryFeePaise;
  final int? totalPaise;
  final int itemCount;
  final bool validForCheckout;
  final String validationStatus;
  final List<CartIssue> issues;
  final List<CommerceCartItem> items;
  factory CommerceCart.fromJson(Map<String, dynamic> json) => CommerceCart(
    id: json['id'] as String? ?? '',
    ownerType: json['owner_type'] as String? ?? 'guest',
    guestToken: json['guest_token'] as String?,
    version: (json['version'] as num?)?.toInt() ?? 1,
    currency: json['currency'] as String? ?? 'INR',
    addressId: json['address_id'] as String?,
    deliveryPincode: json['delivery_pincode'] as String?,
    subtotalPaise: (json['subtotal_paise'] as num?)?.toInt() ?? 0,
    deliveryFeePaise: (json['delivery_fee_paise'] as num?)?.toInt(),
    totalPaise: (json['total_paise'] as num?)?.toInt(),
    itemCount: (json['item_count'] as num?)?.toInt() ?? 0,
    validForCheckout: json['valid_for_checkout'] as bool? ?? false,
    validationStatus: json['validation_status'] as String? ?? 'requires_action',
    issues: (json['issues'] as List<dynamic>? ?? const [])
        .map((item) => CartIssue.fromJson(item as Map<String, dynamic>))
        .toList(growable: false),
    items: (json['items'] as List<dynamic>? ?? const [])
        .map((item) => CommerceCartItem.fromJson(item as Map<String, dynamic>))
        .toList(growable: false),
  );
}

Map<String, dynamic> decodeCachedJson(String value) =>
    jsonDecode(value) as Map<String, dynamic>;
double _double(Object? value) => value is num
    ? value.toDouble()
    : double.tryParse(value?.toString() ?? '') ?? 0;
String _compact(double value) => value == value.roundToDouble()
    ? value.toInt().toString()
    : value.toString();
