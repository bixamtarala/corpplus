import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../models/commerce_api_models.dart';
import '../providers/commerce_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/commerce_state_panel.dart';

class AddressesScreen extends ConsumerStatefulWidget {
  const AddressesScreen({super.key});
  @override
  ConsumerState<AddressesScreen> createState() => _State();
}

class _State extends ConsumerState<AddressesScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(addressControllerProvider.notifier).load());
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final state = ref.watch(addressControllerProvider);
    return Scaffold(
      appBar: AppBar(title: Text(l10n.text('addresses'))),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _edit(context),
        icon: const Icon(Icons.add),
        label: Text(l10n.text('add_address')),
      ),
      body: state.status != LoadStatus.ready && state.items.isEmpty
          ? CommerceStatePanel(
              status: state.status,
              message: state.message,
              onRetry: () =>
                  ref.read(addressControllerProvider.notifier).load(),
            )
          : RefreshIndicator(
              onRefresh: () =>
                  ref.read(addressControllerProvider.notifier).load(),
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  if (state.message != null)
                    Text(
                      state.message!,
                      style: const TextStyle(color: Colors.red),
                    ),
                  for (final address in state.items)
                    Card(
                      child: ListTile(
                        leading: Icon(
                          address.isDefault
                              ? Icons.home
                              : Icons.location_on_outlined,
                          color: AppTheme.primaryGreen,
                        ),
                        title: Text(
                          '${address.label}${address.isDefault ? ' · ${l10n.text('default_address')}' : ''}',
                        ),
                        subtitle: Text(
                          '${address.line1}, ${address.locality}\n${address.district}, ${address.state} ${address.pincode}\n${address.serviceability.reason}',
                        ),
                        isThreeLine: true,
                        onTap: () => ref
                            .read(cartControllerProvider.notifier)
                            .selectAddress(address.id),
                        trailing: PopupMenuButton<String>(
                          onSelected: (value) {
                            if (value == 'edit') _edit(context, address);
                            if (value == 'default') {
                              ref
                                  .read(addressControllerProvider.notifier)
                                  .setDefault(address.id);
                            }
                            if (value == 'delete') {
                              ref
                                  .read(addressControllerProvider.notifier)
                                  .delete(address.id);
                            }
                          },
                          itemBuilder: (_) => [
                            PopupMenuItem(
                              value: 'edit',
                              child: Text(l10n.text('edit')),
                            ),
                            PopupMenuItem(
                              value: 'default',
                              child: Text(l10n.text('make_default')),
                            ),
                            PopupMenuItem(
                              value: 'delete',
                              child: Text(l10n.text('delete')),
                            ),
                          ],
                        ),
                      ),
                    ),
                ],
              ),
            ),
    );
  }

  Future<void> _edit(BuildContext context, [CommerceAddress? address]) async {
    final l10n = AppStrings.of(context);
    final fields = <String, TextEditingController>{
      for (final key in [
        'label',
        'recipient_name',
        'recipient_phone',
        'line1',
        'line2',
        'landmark',
        'locality',
        'district',
        'state',
        'pincode',
      ])
        key: TextEditingController(
          text:
              switch (key) {
                'label' => address?.label,
                'recipient_name' => address?.recipientName,
                'recipient_phone' => address?.recipientPhone,
                'line1' => address?.line1,
                'line2' => address?.line2,
                'landmark' => address?.landmark,
                'locality' => address?.locality,
                'district' => address?.district,
                'state' => address?.state,
                'pincode' => address?.pincode,
                _ => '',
              } ??
              '',
        ),
    };
    final saved = await showDialog<bool>(
      context: context,
      builder: (dialog) => AlertDialog(
        title: Text(
          address == null
              ? l10n.text('add_address')
              : l10n.text('edit_address'),
        ),
        content: SizedBox(
          width: 420,
          child: SingleChildScrollView(
            child: Column(
              children: [
                for (final entry in fields.entries)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 10),
                    child: TextField(
                      controller: entry.value,
                      keyboardType:
                          entry.key == 'pincode' ||
                              entry.key == 'recipient_phone'
                          ? TextInputType.phone
                          : TextInputType.text,
                      decoration: InputDecoration(
                        labelText: l10n.text('address_${entry.key}'),
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialog, false),
            child: Text(l10n.text('cancel')),
          ),
          ElevatedButton(
            onPressed: () async {
              final data = {
                for (final entry in fields.entries)
                  entry.key: entry.value.text.trim(),
                if (address == null) 'make_default': false,
              };
              final ok = await ref
                  .read(addressControllerProvider.notifier)
                  .save(data, id: address?.id);
              if (ok && dialog.mounted) Navigator.pop(dialog, true);
            },
            child: Text(l10n.text('save')),
          ),
        ],
      ),
    );
    for (final controller in fields.values) {
      controller.dispose();
    }
    if (saved == true) {
      await ref.read(addressControllerProvider.notifier).load();
    }
  }
}
