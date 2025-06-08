// ignore_for_file: deprecated_member_use
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
import 'package:smart_rent/api/auth_service.dart';
import 'package:smart_rent/api/property_service.dart';
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';
import 'package:smart_rent/widgets/appbar/drawer.dart';
import 'package:smart_rent/widgets/profile/profile_button.dart';
// import 'package:smart_rent/widgets/profile/profile_container.dart';
import 'package:smart_rent/widgets/profile/profile_property_list.dart';
import 'package:smart_rent/widgets/profile/reserved_property_list.dart';
import 'package:smart_rent/widgets/subtitle.dart';
import 'package:smart_rent/widgets/title.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({
    super.key,
    required this.token,
  });

  final String token;

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  String currentView = 'active';
  final ScrollController _scrollController = ScrollController();

  String userName = '';
  String userEmail = '';
  bool isLoadingUser = true;

  @override
  void initState() {
    super.initState();
    fetchUserInfo();
  }

  Future<void> fetchUserInfo() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:8002/api/me'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          userName = data['name'] ?? 'Nieznany';
          userEmail = data['email'] ?? 'brak@domena.pl';
          isLoadingUser = false;
        });
      } else {
        setState(() {
          userName = 'Błąd użytkownika';
          userEmail = 'Nie udało się pobrać e-maila';
          isLoadingUser = false;
        });
      }
    } catch (e) {
      setState(() {
        userName = 'Błąd połączenia';
        userEmail = 'Brak danych';
        isLoadingUser = false;
      });
    }
  }

  void showApartments(String type) {
    setState(() {
      currentView = type;
    });
  }

  void _showAddPropertyDialog(String token) {
    final _descriptionController = TextEditingController();
    final _adressController = TextEditingController();
    final _priceController = TextEditingController();
    final _statusController = TextEditingController(text: 'Active');

    showDialog(
      context: context,
      builder: (ctx) {
        return AlertDialog(
          title: const Text('Add Apartment'),
          content: SingleChildScrollView(
            child: Column(
              children: [
                TextField(
                  controller: _descriptionController,
                  decoration: const InputDecoration(labelText: 'Description'),
                ),
                TextField(
                  controller: _adressController,
                  decoration: const InputDecoration(labelText: 'Address'),
                ),
                TextField(
                  controller: _priceController,
                  decoration: const InputDecoration(labelText: 'Price'),
                  keyboardType: TextInputType.number,
                ),
                TextField(
                  controller: _statusController,
                  decoration: const InputDecoration(labelText: 'Status'),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              child: const Text('Back'),
              onPressed: () => Navigator.of(ctx).pop(),
            ),
            ElevatedButton(
              child: const Text('Save'),
              onPressed: () async {
                final description = _descriptionController.text.trim();
                final adress = _adressController.text.trim();
                final price = double.tryParse(_priceController.text) ?? 0.0;
                final status = _statusController.text.trim();

                final result = await addProperty(
                  token,
                  description,
                  price,
                  status,
                  adress,
                );

                Navigator.of(ctx).pop();

                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content:
                          Text(result['message'] ?? result['error'] ?? 'Błąd'),
                    ),
                  );
                  setState(() {});
                  WidgetsBinding.instance.addPostFrameCallback((_) {
                    if (_scrollController.hasClients) {
                      _scrollController.animateTo(
                        _scrollController.position.maxScrollExtent,
                        duration: const Duration(milliseconds: 500),
                        curve: Curves.easeOut,
                      );
                    }
                  });
                }
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final token = Provider.of<AuthProvider>(context).token;

    return Scaffold(
      backgroundColor: SRAppColors.backgroundColor,
      appBar: AppBar(
        backgroundColor: SRAppColors.backgroundColor,
        title: Text('Profile', style: SRAppFonst.title),
      ),
      drawer: SRDrawer(),
      body: Padding(
        padding: const EdgeInsets.all(5.0),
        child: Column(
          children: [
            // isLoadingUser
            //     ? const CircularProgressIndicator()
            //     : SRProfileContainer(
            //         userName: userName,
            //         userEmail: userEmail,
            //       ),
            const Divider(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                SRProfileButton(
                  buttonTxt: 'Your Apartments',
                  onPressed: () => showApartments('active'),
                  isSelected: currentView == 'active',
                ),
                SRProfileButton(
                  buttonTxt: 'Reserved',
                  onPressed: () => showApartments('reserved'),
                  isSelected: currentView == 'reserved',
                ),
              ],
            ),
            const Divider(),
            Expanded(
              child: currentView == 'active'
                  ? ProfilePropertyList(
                      token: token,
                      scrollController: _scrollController,
                    )
                  : ReservedPropertyList(
                      token: token,
                      scrollController: _scrollController,
                    ),
            ),
          ],
        ),
      ),
      floatingActionButton: currentView == 'active'
          ? FloatingActionButton(
              onPressed: () => _showAddPropertyDialog(token),
              child: const Icon(Icons.add),
            )
          : null,
    );
  }
}

class SRApartmentWidget extends StatelessWidget {
  const SRApartmentWidget({
    super.key,
    required this.apartmentCountry,
    required this.apartmentAddress,
    required this.apartmentStatus,
    required this.apartmentOwner,
  });

  final String apartmentCountry;
  final String apartmentAddress;
  final String apartmentStatus;
  final String apartmentOwner;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      margin: EdgeInsets.all(5),
      decoration: BoxDecoration(
        color: SRAppColors.backgroundColor,
        border: Border.all(color: SRAppColors.borderColor, width: 2),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            spreadRadius: 2,
            blurRadius: 6,
            offset: const Offset(2, 4),
          ),
        ],
      ),
      child: Column(
        children: [
          Row(
            children: [
              SRTitle(titleTxt: apartmentCountry),
            ],
          ),
          Divider(),
          Row(
            children: [
              SRSubTitle(titleTxt: 'Address:'),
            ],
          ),
          Row(
            children: [
              Expanded(
                child: Text(
                  // "Carrer de Santa Fe de Nou Mèxic, s/n, Sarrià-Sant Gervasi, 08021 Barcelona",
                  apartmentAddress,
                  style: SRAppFonst.customSizeLightTxt,
                  textAlign: TextAlign.center,
                  softWrap: true,
                ),
              ),
            ],
          ),
          Row(
            children: [
              SRSubTitle(titleTxt: 'Status:'),
              Text(
                // 'Active',
                apartmentStatus,
                style: SRAppFonst.customSizeLightTxt,
                textAlign: TextAlign.center,
              ),
            ],
          ),
          Row(
            children: [
              SRSubTitle(titleTxt: 'Apartmanet owner: '),
              Text(
                // "IgorUchnast",
                apartmentOwner,
                style: SRAppFonst.customSizeLightTxt,
                textAlign: TextAlign.center,
              ),
            ],
          ),
          Divider(),
        ],
      ),
    );
  }
}
