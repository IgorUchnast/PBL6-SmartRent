import 'package:flutter/material.dart';
import 'package:smart_rent/config/colors.dart';
import 'package:smart_rent/config/fonts.dart';
import 'package:smart_rent/widgets/appbar/drawer.dart';
import 'package:smart_rent/widgets/control_panel/animated_container.dart';
import 'package:smart_rent/widgets/control_panel/device_list.dart';
import 'package:smart_rent/widgets/control_panel/outlet_button.dart';
import 'package:smart_rent/widgets/control_panel/temperature_chart.dart';

class SingleApartmentPage extends StatefulWidget {
  const SingleApartmentPage({super.key});

  @override
  State<SingleApartmentPage> createState() => _SingleApartmentPageState();
}

class _SingleApartmentPageState extends State<SingleApartmentPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: SRAppColors.backgroundColor,
      appBar: AppBar(
        backgroundColor: SRAppColors.backgroundColor,
        title: Text(
          'Control Panel',
          style: SRAppFonst.title,
        ),
      ),
      drawer: SRDrawer(),
      body: Container(
        padding: EdgeInsets.all(10),
        child: SingleChildScrollView(
          child: Column(
            children: [
              Divider(),
              ExpandableOutletSection(
                sectionName: 'Outlet',
                sectionContainer: SRPowerButtonScreen(),
                deviceList: [
                  Device(id: '1', name: 'Outlet Kitchen'),
                  Device(id: '2', name: 'Outlet Livingroom'),
                  Device(id: '3', name: 'Outlet Bathroom'),
                ],
              ),
              ExpandableOutletSection(
                sectionName: 'Charts',
                sectionContainer: SRTemperatureChart(),
                deviceList: [
                  Device(id: '1', name: 'Temperature'),
                  Device(id: '2', name: 'Humidity'),
                  Device(id: '3', name: 'Energy consumption'),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class SRDeviceContainer extends StatelessWidget {
  const SRDeviceContainer({super.key});

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
