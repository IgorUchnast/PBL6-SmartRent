import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:smart_rent/api/config.dart';
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

  Future<List<Item>> fetchItemsFromApi() async {
    final response = await http.get(
      Uri.parse('$service2/api/all-properties'),
    );

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = jsonDecode(response.body);
      return jsonList.map((item) => Item.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load properties');
    }
  }

  Future<void> reserveProperty(int propertyId) async {
    final response = await http.post(
      Uri.parse('$service2/api/reserve'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'property_id': propertyId,
        'start_date': DateTime.now().toIso8601String(),
        'end_date':
            DateTime.now().add(const Duration(days: 3)).toIso8601String(),
      }),
    );

    if (response.statusCode == 201) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Rezerwacja udana")),
      );
      final updatedItems = await fetchItemsFromApi();
      setState(() {
        futureItems = Future.value(updatedItems);
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Błąd rezerwacji: ${response.body}")),
      );
    }
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
          return const Center(child: Text('Brak dostępnych mieszkań'));
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
                title: Text(item.name, style: SRAppFonst.subtitle),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Divider(),
                    Text('Price: \$${item.price.toStringAsFixed(2)}',
                        style: SRAppFonst.darkTxt),
                    Text('Status: ${item.status}', style: SRAppFonst.darkTxt),
                    Text('Description: ${item.description}',
                        style: SRAppFonst.darkTxt),
                  ],
                ),
                trailing: ElevatedButton(
                  onPressed: item.status == 'Active'
                      ? () => reserveProperty(item.id)
                      : null,
                  child: const Text("Book"),
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
  final int id;
  final String name;
  final double price;
  final String status;
  final String description;

  Item({
    required this.id,
    required this.name,
    required this.price,
    required this.status,
    required this.description,
  });

  factory Item.fromJson(Map<String, dynamic> json) {
    return Item(
      id: json['id'],
      name: json['name'] ?? 'Apartment',
      price: (json['price'] as num).toDouble(),
      status: json['status'],
      description: json['description'],
    );
  }
}
