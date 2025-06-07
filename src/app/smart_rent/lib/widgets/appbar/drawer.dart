import 'package:flutter/material.dart';
import 'package:smart_rent/api/auth_service.dart';
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';
import 'package:smart_rent/pages/apartment_page.dart';
import 'package:smart_rent/pages/home_page.dart';
import 'package:smart_rent/pages/profile_page.dart';
import 'package:smart_rent/pages/settings_page.dart';
import 'package:smart_rent/widgets/subtitle.dart';
import 'package:provider/provider.dart';

class SRDrawer extends StatefulWidget {
  const SRDrawer({super.key});

  @override
  State<SRDrawer> createState() => _SRDrawerState();
}

class _SRDrawerState extends State<SRDrawer> {
  @override
  Widget build(BuildContext context) {
    final token = Provider.of<AuthProvider>(context).token;
    // final userId = Provider.of<AuthProvider>(context).userId;
    return Drawer(
      child: Container(
        color: SRAppColors.backgroundColor,
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(
                color: SRAppColors.backgroundColor,
              ),
              child: Column(
                children: [
                  Row(
                    children: [
                      Text(
                        'Smart Rent',
                        style: SRAppFonst.title,
                      ),
                    ],
                  ),
                  Row(
                    children: [
                      SRSubTitle(titleTxt: "Name:"),
                      Text(
                        'IgorUchnast',
                        style: SRAppFonst.drawerTxt,
                      ),
                    ],
                  ),
                  Row(
                    children: [
                      SRSubTitle(titleTxt: "Email:"),
                      Text(
                        'igor.uchnast@gmail.com',
                        style: SRAppFonst.drawerTxt,
                      ),
                    ],
                  )
                ],
              ),
            ),
            ListTile(
              leading: const Icon(Icons.person),
              title: Text(
                'Profile',
                style: SRAppFonst.darkTxt,
              ),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ProfilePage(token: token),
                  ),
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.home),
              title: Text(
                'Home Page',
                style: SRAppFonst.darkTxt,
              ),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const HomePage()),
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.access_time_outlined),
              title: Text(
                'Current Apartments',
                style: SRAppFonst.darkTxt,
              ),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => const ApartmentPage()),
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.monetization_on_outlined),
              title: Text(
                'Billings',
                style: SRAppFonst.darkTxt,
              ),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const SettingsPage()),
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.settings),
              title: Text(
                'Settings',
                style: SRAppFonst.darkTxt,
              ),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const SettingsPage()),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
