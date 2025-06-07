// ignore_for_file: deprecated_member_use
import 'package:flutter/material.dart';
import 'package:smart_rent/api/property_service.dart' as propertyService;
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';
import 'package:smart_rent/widgets/appbar/drawer.dart';
import 'package:smart_rent/widgets/profile/profile_button.dart';
import 'package:smart_rent/widgets/profile/profile_container.dart';
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

  void showApartments(String type) {
    setState(() {
      currentView = type;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: SRAppColors.backgroundColor,
      appBar: AppBar(
        backgroundColor: SRAppColors.backgroundColor,
        title: Text(
          'Profile',
          style: SRAppFonst.title,
        ),
      ),
      drawer: SRDrawer(),
      body: Padding(
        padding: const EdgeInsets.all(5.0),
        child: Column(
          children: [
            SRProfileContainer(
              userName: 'IgorUchnast',
              userEmail: 'igor.uchnast@gmail.com',
            ),
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
                  buttonTxt: 'Apartments History',
                  onPressed: () => showApartments('history'),
                  isSelected: currentView == 'history',
                ),
              ],
            ),
            const Divider(),
            Expanded(
              child: _buildView(currentView),
            ),
          ],
        ),
      ),
      floatingActionButton: ElevatedButton(
        onPressed: () async {
          final result = await propertyService.addProperty(
            widget.token, // JWT token po zalogowaniu
            "Nowe mieszkanie na wynajem",
            120.0,
          );

          if (result['message'] == "Property added successfully") {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Dodano mieszkanie')),
            );
          } else {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(result['error'] ?? 'Błąd')),
            );
          }
        },
        child: Text("Dodaj mieszkanie"),
      ),
    );
  }

  Widget _buildView(String type) {
    switch (type) {
      case 'active':
        return _buildActiveApartments();
      case 'history':
        return _buildHistoryApartments();
      default:
        return const Center(child: Text("Wybierz kategorię powyżej"));
    }
  }

  Widget _buildActiveApartments() {
    return ListView(
      children: const [
        ListTile(
            title: SRApartmentWidget(
          apartmentCountry: 'Spain',
          apartmentAddress:
              'Carrer de Santa Fe de Nou Mèxic, s/n, Sarrià-Sant Gervasi, 08021 Barcelona',
          apartmentStatus: 'Active',
          apartmentOwner: 'IgorUchnast',
        )),
        ListTile(
            title: SRApartmentWidget(
          apartmentCountry: 'Portugal',
          apartmentAddress:
              'Carrer de Santa Fe de Nou Mèxic, s/n, Sarrià-Sant Gervasi, 08021 Lisboa',
          apartmentStatus: 'Occupied',
          apartmentOwner: 'IgorUchnast',
        )),
      ],
    );
  }

  Widget _buildHistoryApartments() {
    return ListView(
      children: const [
        ListTile(
          title: SRApartmentWidget(
            apartmentCountry: 'Greece',
            apartmentAddress:
                'Carrer de Santa Fe de Nou Mèxic, s/n, Sarrià-Sant Gervasi, 08021 Barcelona',
            apartmentStatus: 'Active',
            apartmentOwner: 'IgorUchnast',
          ),
        ),
        ListTile(
          title: SRApartmentWidget(
            apartmentCountry: 'France',
            apartmentAddress:
                'Carrer de Santa Fe de Nou Mèxic, s/n, Sarrià-Sant Gervasi, 08021 Lisboa',
            apartmentStatus: 'Occupied',
            apartmentOwner: 'IgorUchnast',
          ),
        ),
      ],
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
