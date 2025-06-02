import 'package:flutter/material.dart';
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';

class ApiListPage extends StatefulWidget {
  const ApiListPage({super.key});

  @override
  State<ApiListPage> createState() => _ApiListPageState();
}

class _ApiListPageState extends State<ApiListPage> {
  late Future<List<Item>> futureItems;

  @override
  void initState() {
    super.initState();
    futureItems = fetchItemsFromApi();
  }

  // 🧪 Symulowane API
  Future<List<Item>> fetchItemsFromApi() async {
    await Future.delayed(const Duration(seconds: 2));
    return [
      Item(
          name: 'Spain',
          price: 59.99,
          status: 'Active',
          description: 'Les Corts, 08028 Barcelona, Hiszpania'),
      Item(
          name: 'Portugal',
          price: 249.00,
          status: 'Inactive',
          description:
              'Carrer del Vallespir, 194, Les Corts, 08014 Barcelona, Hiszpania'),
      Item(
          name: 'France',
          price: 99.99,
          status: 'Active',
          description:
              'Carrer del Vallespir, 194, Les Corts, 08014 Barcelona, Hiszpania'),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Item>>(
      future: futureItems,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(child: Text('Błąd: ${snapshot.error}'));
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return const Center(child: Text('Brak danych'));
        }

        final items = snapshot.data!;
        return ListView.builder(
          itemCount: items.length,
          itemBuilder: (context, index) {
            final item = items[index];
            return Card(
              color: SRAppColors.backgroundColor,
              margin: const EdgeInsets.all(10),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
                side: BorderSide(color: SRAppColors.borderColor),
              ),
              child: ListTile(
                title: Text(
                  item.name,
                  style: SRAppFonst.subtitle,
                ),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Divider(),
                    Text(
                      'Price: \$${item.price.toStringAsFixed(2)}',
                      style: SRAppFonst.darkTxt,
                    ),
                    Text(
                      'Status: ${item.status}',
                      style: SRAppFonst.darkTxt,
                    ),
                    Text(
                      'Description: ${item.description}',
                      style: SRAppFonst.darkTxt,
                    ),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }
}

class Item {
  final String name;
  final double price;
  final String status;
  final String description;

  Item({
    required this.name,
    required this.price,
    required this.status,
    required this.description,
  });
}
