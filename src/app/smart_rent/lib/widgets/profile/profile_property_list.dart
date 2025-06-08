import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';

class ProfilePropertyList extends StatefulWidget {
  const ProfilePropertyList({
    super.key,
    required this.token,
    required ScrollController scrollController,
  });
  final String token;
  @override
  State<ProfilePropertyList> createState() => _ProfilePropertyListState();
}

class _ProfilePropertyListState extends State<ProfilePropertyList> {
  late Future<List<Item>> futureItems;
  @override
  void initState() {
    super.initState();
    futureItems = fetchUserProperties(widget.token);
  }

  Future<List<Item>> fetchUserProperties(String token) async {
    final response = await http.get(
      Uri.parse('http://localhost:8002/api/properties'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = jsonDecode(response.body);
      return jsonList.map((item) => Item.fromJson(item)).toList();
    } else {
      throw Exception('Nie udało się pobrać mieszkań użytkownika');
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
                title: Text(
                  item.name,
                  style: SRAppFonst.subtitle,
                ),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Divider(),
                    Text(
                      'Cena: \$${item.price.toStringAsFixed(2)}',
                      style: SRAppFonst.darkTxt,
                    ),
                    Text(
                      'Status: ${item.status}',
                      style: SRAppFonst.darkTxt,
                    ),
                    Text(
                      'Opis: ${item.description}',
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

  factory Item.fromJson(Map<String, dynamic> json) {
    return Item(
      name: json['name'] ?? 'Apartament for rent',
      price: (json['price'] as num).toDouble(),
      status: json['status'],
      description: json['description'],
    );
  }
}
