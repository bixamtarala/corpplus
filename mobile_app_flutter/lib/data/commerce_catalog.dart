import '../models/commerce_product.dart';

class CommerceCatalog {
  static const categories = [
    CommerceCategory(
      id: 'vegetables',
      label: 'Vegetables',
      iconName: 'vegetable',
    ),
    CommerceCategory(id: 'fruits', label: 'Fruits', iconName: 'fruit'),
    CommerceCategory(id: 'greens', label: 'Leafy greens', iconName: 'greens'),
    CommerceCategory(id: 'grains', label: 'Rice & millets', iconName: 'grain'),
    CommerceCategory(id: 'pulses', label: 'Pulses', iconName: 'pulses'),
    CommerceCategory(id: 'spices', label: 'Spices', iconName: 'spices'),
  ];

  static const products = [
    CommerceProduct(
      id: 'tomato-grade-a-1kg',
      name: 'Tomato',
      localizedNames: {'hi': 'टमाटर', 'te': 'టమాటా'},
      category: 'vegetables',
      packLabel: '1 kg',
      previewPricePaise: 4200,
      grade: 'Grade A preview',
      origin: 'Source to be assigned',
      description:
          'Standardized pilot pack. Final source, grade, availability, and price require operations approval.',
      isFresh: true,
    ),
    CommerceProduct(
      id: 'onion-1kg',
      name: 'Onion',
      localizedNames: {'hi': 'प्याज', 'te': 'ఉల్లిపాయ'},
      category: 'vegetables',
      packLabel: '1 kg',
      previewPricePaise: 3600,
      grade: 'Pilot grade pending',
      origin: 'Source to be assigned',
      description: 'Preview catalog item for the controlled commerce pilot.',
      isFresh: true,
    ),
    CommerceProduct(
      id: 'potato-1kg',
      name: 'Potato',
      localizedNames: {'hi': 'आलू', 'te': 'బంగాళాదుంప'},
      category: 'vegetables',
      packLabel: '1 kg',
      previewPricePaise: 3200,
      grade: 'Pilot grade pending',
      origin: 'Source to be assigned',
      description: 'Preview catalog item for the controlled commerce pilot.',
      isFresh: true,
    ),
    CommerceProduct(
      id: 'banana-robusta-1kg',
      name: 'Banana',
      localizedNames: {'hi': 'केला', 'te': 'అరటిపండు'},
      category: 'fruits',
      packLabel: '1 kg',
      previewPricePaise: 5800,
      grade: 'Robusta preview',
      origin: 'Source to be assigned',
      description: 'Indicative fresh-fruit SKU. Live fulfilment is not active.',
      isFresh: true,
    ),
    CommerceProduct(
      id: 'papaya-1piece',
      name: 'Papaya',
      localizedNames: {'hi': 'पपीता', 'te': 'బొప్పాయి'},
      category: 'fruits',
      packLabel: '1 piece',
      previewPricePaise: 6500,
      grade: 'Pilot grade pending',
      origin: 'Source to be assigned',
      description:
          'Indicative fresh-fruit SKU. Actual piece weight will require a defined pilot standard.',
      isFresh: true,
    ),
    CommerceProduct(
      id: 'spinach-1bunch',
      name: 'Spinach',
      localizedNames: {'hi': 'पालक', 'te': 'పాలకూర'},
      category: 'greens',
      packLabel: '1 bunch',
      previewPricePaise: 2500,
      grade: 'Pilot grade pending',
      origin: 'Source to be assigned',
      description: 'Indicative leafy-green SKU for layout and cart validation.',
      isFresh: true,
    ),
    CommerceProduct(
      id: 'coriander-1bunch',
      name: 'Coriander leaves',
      localizedNames: {'hi': 'धनिया पत्ती', 'te': 'కొత్తిమీర'},
      category: 'greens',
      packLabel: '1 bunch',
      previewPricePaise: 1800,
      grade: 'Pilot grade pending',
      origin: 'Source to be assigned',
      description: 'Indicative leafy-green SKU for layout and cart validation.',
      isFresh: true,
    ),
    CommerceProduct(
      id: 'sona-masoori-rice-5kg',
      name: 'Sona Masoori rice',
      localizedNames: {'hi': 'सोना मसूरी चावल', 'te': 'సోనా మసూరి బియ్యం'},
      category: 'grains',
      packLabel: '5 kg',
      previewPricePaise: 34500,
      grade: 'Pack declaration pending',
      origin: 'Supplier to be assigned',
      description:
          'Preview packaged-staple SKU. Seller and mandatory declarations must be approved before sale.',
    ),
    CommerceProduct(
      id: 'ragi-1kg',
      name: 'Ragi',
      localizedNames: {'hi': 'रागी', 'te': 'రాగులు'},
      category: 'grains',
      packLabel: '1 kg',
      previewPricePaise: 7200,
      grade: 'Pack declaration pending',
      origin: 'Supplier to be assigned',
      description: 'Preview millet SKU. Live availability is not active.',
    ),
    CommerceProduct(
      id: 'toor-dal-1kg',
      name: 'Toor dal',
      localizedNames: {'hi': 'अरहर दाल', 'te': 'కందిపప్పు'},
      category: 'pulses',
      packLabel: '1 kg',
      previewPricePaise: 16800,
      grade: 'Pack declaration pending',
      origin: 'Supplier to be assigned',
      description: 'Preview pulse SKU. Live availability is not active.',
    ),
    CommerceProduct(
      id: 'chana-dal-1kg',
      name: 'Chana dal',
      localizedNames: {'hi': 'चना दाल', 'te': 'శనగపప్పు'},
      category: 'pulses',
      packLabel: '1 kg',
      previewPricePaise: 9800,
      grade: 'Pack declaration pending',
      origin: 'Supplier to be assigned',
      description: 'Preview pulse SKU. Live availability is not active.',
    ),
    CommerceProduct(
      id: 'turmeric-powder-200g',
      name: 'Turmeric powder',
      localizedNames: {'hi': 'हल्दी पाउडर', 'te': 'పసుపు పొడి'},
      category: 'spices',
      packLabel: '200 g',
      previewPricePaise: 6400,
      grade: 'Pack declaration pending',
      origin: 'Supplier to be assigned',
      description:
          'Preview spice SKU. Claims and packaged-product declarations require approval.',
    ),
  ];

  static CommerceCategory categoryById(String id) =>
      categories.firstWhere((category) => category.id == id);

  static List<CommerceProduct> productsForCategory(String? categoryId) {
    if (categoryId == null) {
      return products;
    }
    return products.where((product) => product.category == categoryId).toList();
  }

  static List<CommerceProduct> search(String query) {
    final normalized = query.trim().toLowerCase();
    if (normalized.isEmpty) {
      return products;
    }
    return products.where((product) {
      return product.name.toLowerCase().contains(normalized) ||
          product.localizedNames.values.any(
            (name) => name.toLowerCase().contains(normalized),
          ) ||
          categoryById(
            product.category,
          ).label.toLowerCase().contains(normalized);
    }).toList();
  }
}
