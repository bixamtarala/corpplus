import 'package:flutter/material.dart';

import '../data/commodity_catalog.dart';
import '../theme/app_theme.dart';

class CommoditySelectorField extends StatelessWidget {
  const CommoditySelectorField({
    super.key,
    required this.value,
    required this.onChanged,
    required this.labelText,
  });

  final String value;
  final ValueChanged<String> onChanged;
  final String labelText;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(10),
      onTap: () async {
        final selected = await showModalBottomSheet<String>(
          context: context,
          isScrollControlled: true,
          backgroundColor: Colors.transparent,
          builder: (_) => _CommodityPickerSheet(initialValue: value),
        );

        if (selected != null && selected != value) {
          onChanged(selected);
        }
      },
      child: InputDecorator(
        decoration: InputDecoration(
          labelText: labelText,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
          suffixIcon: const Icon(Icons.search),
        ),
        child: Row(
          children: [
            Expanded(
              child: Text(
                value,
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
              ),
            ),
            const Icon(Icons.arrow_drop_down),
          ],
        ),
      ),
    );
  }
}

class _CommodityPickerSheet extends StatefulWidget {
  const _CommodityPickerSheet({required this.initialValue});

  final String initialValue;

  @override
  State<_CommodityPickerSheet> createState() => _CommodityPickerSheetState();
}

class _CommodityPickerSheetState extends State<_CommodityPickerSheet> {
  static const String _allCategories = 'All Categories';
  static const String _allStates = 'All States';

  final TextEditingController _searchController = TextEditingController();
  String _selectedCategory = _allCategories;
  String _selectedState = _allStates;

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final filteredEntries = CommodityCatalog.search(
      query: _searchController.text,
      category: _selectedCategory == _allCategories ? null : _selectedCategory,
      state: _selectedState == _allStates ? null : _selectedState,
    );

    final groupedEntries = <String, List<CommodityEntry>>{};
    for (final entry in filteredEntries) {
      groupedEntries.putIfAbsent(entry.category, () => []).add(entry);
    }

    final mediaQuery = MediaQuery.of(context);

    return SafeArea(
      child: Padding(
        padding: EdgeInsets.only(top: mediaQuery.size.height * 0.08),
        child: Material(
          color: Colors.white,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
          child: SizedBox(
            height: mediaQuery.size.height * 0.86,
            child: Column(
              children: [
                const SizedBox(height: 12),
                Container(
                  width: 48,
                  height: 5,
                  decoration: BoxDecoration(
                    color: AppTheme.lightGray,
                    borderRadius: BorderRadius.circular(999),
                  ),
                ),
                const SizedBox(height: 16),
                const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 20),
                  child: Row(
                    children: [
                      Expanded(
                        child: Text(
                          'Select Commodity',
                          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  child: TextField(
                    controller: _searchController,
                    onChanged: (_) => setState(() {}),
                    decoration: InputDecoration(
                      hintText: 'Search by crop, category, or state',
                      prefixIcon: const Icon(Icons.search),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(14),
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 14),
                _FilterChipRow(
                  title: 'Category',
                  values: [_allCategories, ...CommodityCatalog.categories],
                  selectedValue: _selectedCategory,
                  onSelected: (value) {
                    setState(() {
                      _selectedCategory = value;
                    });
                  },
                ),
                const SizedBox(height: 10),
                _FilterChipRow(
                  title: 'State',
                  values: [_allStates, ...CommodityCatalog.allStates],
                  selectedValue: _selectedState,
                  onSelected: (value) {
                    setState(() {
                      _selectedState = value;
                    });
                  },
                ),
                const SizedBox(height: 12),
                Expanded(
                  child: groupedEntries.isEmpty
                      ? const Center(
                          child: Text(
                            'No commodities match this search.',
                            style: TextStyle(color: AppTheme.lightText),
                          ),
                        )
                      : ListView(
                          padding: const EdgeInsets.fromLTRB(20, 0, 20, 24),
                          children: [
                            for (final category in CommodityCatalog.categories)
                              if (groupedEntries.containsKey(category)) ...[
                                Padding(
                                  padding: const EdgeInsets.only(top: 16, bottom: 8),
                                  child: Text(
                                    category,
                                    style: const TextStyle(
                                      fontSize: 16,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                                for (final entry in groupedEntries[category]!)
                                  Card(
                                    margin: const EdgeInsets.only(bottom: 10),
                                    elevation: 0,
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(14),
                                      side: BorderSide(
                                        color: entry.name == widget.initialValue
                                            ? AppTheme.primaryGreen
                                            : AppTheme.lightGray,
                                      ),
                                    ),
                                    child: ListTile(
                                      onTap: () => Navigator.of(context).pop(entry.name),
                                      title: Text(entry.name),
                                      subtitle: Text(
                                        entry.states.join(' • '),
                                        maxLines: 2,
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                      trailing: entry.name == widget.initialValue
                                          ? const Icon(
                                              Icons.check_circle,
                                              color: AppTheme.primaryGreen,
                                            )
                                          : const Icon(Icons.chevron_right),
                                    ),
                                  ),
                              ],
                          ],
                        ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _FilterChipRow extends StatelessWidget {
  const _FilterChipRow({
    required this.title,
    required this.values,
    required this.selectedValue,
    required this.onSelected,
  });

  final String title;
  final List<String> values;
  final String selectedValue;
  final ValueChanged<String> onSelected;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Text(
            title,
            style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
          ),
        ),
        const SizedBox(height: 8),
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Row(
            children: [
              for (final value in values)
                Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: ChoiceChip(
                    label: Text(value),
                    selected: selectedValue == value,
                    onSelected: (_) => onSelected(value),
                  ),
                ),
            ],
          ),
        ),
      ],
    );
  }
}