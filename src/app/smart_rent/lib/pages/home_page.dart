import 'package:flutter/material.dart';
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';
import 'package:smart_rent/widgets/appbar/drawer.dart';
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
        title: Text(
          'Smart Rent',
          style: SRAppFonst.title,
        ),
      ),
      drawer: SRDrawer(),
      body: Container(
        color: SRAppColors.backgroundColor,
        child: Column(
          children: [
            SRTitle(titleTxt: 'Apartments for Rent'),
            Expanded(
              child: ApiListPage(),
            ),
          ],
        ),
      ),
    );
  }
}
