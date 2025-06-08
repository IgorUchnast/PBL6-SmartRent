import 'package:flutter/material.dart';
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';
import 'package:smart_rent/widgets/appbar/drawer.dart'; // Dodaj właściwą ścieżkę do ApiListPage
import 'package:smart_rent/widgets/homePage/table_list.dart';
import 'package:smart_rent/widgets/title.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: SRAppColors.backgroundColor,
      appBar: AppBar(
        backgroundColor: SRAppColors.backgroundColor,
        elevation: 0,
        title: Text(
          'Smart Rent',
          style: SRAppFonst.title,
        ),
        centerTitle: true,
      ),
      drawer: const SRDrawer(),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: const [
          Padding(
            padding: EdgeInsets.all(16.0),
            child: SRTitle(titleTxt: 'Apartments for Rent'),
          ),
          Expanded(
            child: ApiListPage(),
          ),
        ],
      ),
    );
  }
}
