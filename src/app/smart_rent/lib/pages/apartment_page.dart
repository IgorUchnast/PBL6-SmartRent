import 'package:flutter/material.dart';
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';
import 'package:smart_rent/pages/profile_page.dart';
import 'package:smart_rent/pages/single_apartment_page.dart';
import 'package:smart_rent/widgets/appbar/drawer.dart';
import 'package:smart_rent/widgets/title.dart';

class ApartmentPage extends StatelessWidget {
  const ApartmentPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: SRAppColors.backgroundColor,
      appBar: AppBar(
        backgroundColor: SRAppColors.backgroundColor,
        title: Text(
          'Currnet Appartments',
          style: SRAppFonst.title,
        ),
      ),
      drawer: SRDrawer(),
      body: Container(
        padding: EdgeInsets.all(10),
        child: SingleChildScrollView(
          child: Column(
            children: [
              SRTitle(titleTxt: 'Currently rented apartment'),
              GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => const SingleApartmentPage()),
                  );
                },
                child: SRApartmentWidget(
                  apartmentCountry: 'Portugal',
                  apartmentAddress:
                      'Carrer de Santa Fe de Nou Mèxic, s/n, Sarrià-Sant Gervasi, 08021 Lisboa',
                  apartmentStatus: 'Occupied',
                  apartmentOwner: 'IgorUchnast',
                ),
              ),
              SRTitle(titleTxt: 'Apartments booked'),
              SRApartmentWidget(
                apartmentCountry: 'Portugal',
                apartmentAddress:
                    'Carrer de Santa Fe de Nou Mèxic, s/n, Sarrià-Sant Gervasi, 08021 Lisboa',
                apartmentStatus: 'Occupied',
                apartmentOwner: 'IgorUchnast',
              ),
              SRApartmentWidget(
                apartmentCountry: 'Portugal',
                apartmentAddress:
                    'Carrer de Santa Fe de Nou Mèxic, s/n, Sarrià-Sant Gervasi, 08021 Lisboa',
                apartmentStatus: 'Occupied',
                apartmentOwner: 'IgorUchnast',
              ),
            ],
          ),
        ),
      ),
    );
  }
}
