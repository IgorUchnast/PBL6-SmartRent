import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';
import 'package:smart_rent/pages/single_apartment_page.dart';

class ReservedPropertyList extends StatefulWidget {
  const ReservedPropertyList({
    super.key,
    required this.token,
    required this.scrollController,
  });

  final String token;
  final ScrollController scrollController;

  @override
  State<ReservedPropertyList> createState() => _ReservedPropertyListState();
}

class _ReservedPropertyListState extends State<ReservedPropertyList> {
  late Future<List<ReservationItem>> futureItems;

  @override
  void initState() {
    super.initState();
    futureItems = fetchReservations(widget.token);
  }

  Future<List<ReservationItem>> fetchReservations(String token) async {
    final response = await http.get(
      Uri.parse('http://localhost:8002/api/reservations'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = jsonDecode(response.body);
      return jsonList.map((item) => ReservationItem.fromJson(item)).toList();
    } else {
      throw Exception('Nie udało się pobrać rezerwacji');
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<ReservationItem>>(
      future: futureItems,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(child: Text('Błąd: ${snapshot.error}'));
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return const Center(child: Text('Brak aktywnych rezerwacji'));
        }

        final items = snapshot.data!;
        return ListView.builder(
          controller: widget.scrollController,
          itemCount: items.length,
          itemBuilder: (context, index) {
            final item = items[index];
            return GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => SingleApartmentPage(),
                  ),
                );
              },
              child: Card(
                color: SRAppColors.backgroundColor,
                margin: const EdgeInsets.all(10),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                  side: BorderSide(color: SRAppColors.borderColor),
                ),
                child: ListTile(
                  title: Text('Reservation #${item.id}',
                      style: SRAppFonst.subtitle),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Divider(),
                      Text('Apartment ID: ${item.propertyId}',
                          style: SRAppFonst.darkTxt),
                      Text('Status: ${item.status}', style: SRAppFonst.darkTxt),
                      Text('Start date: ${item.startDate}',
                          style: SRAppFonst.darkTxt),
                      Text('End date: ${item.endDate}',
                          style: SRAppFonst.darkTxt),
                    ],
                  ),
                ),
              ),
            );
          },
        );
      },
    );
  }
}

class ReservationItem {
  final int id;
  final int propertyId;
  final String status;
  final String startDate;
  final String endDate;

  ReservationItem({
    required this.id,
    required this.propertyId,
    required this.status,
    required this.startDate,
    required this.endDate,
  });

  factory ReservationItem.fromJson(Map<String, dynamic> json) {
    return ReservationItem(
      id: json['id'],
      propertyId: json['property_id'],
      status: json['status'] ?? 'pending',
      startDate: json['start_date'],
      endDate: json['end_date'],
    );
  }
}
