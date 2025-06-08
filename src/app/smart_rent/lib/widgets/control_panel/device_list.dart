import 'package:flutter/material.dart';

class Device {
  final String name;
  final String id;

  Device({required this.name, required this.id});
}

// ignore: must_be_immutable
class DeviceDropdownPage extends StatefulWidget {
  DeviceDropdownPage({
    super.key,
    required this.deviceList,
  });

  List<Device> deviceList;
  @override
  State<DeviceDropdownPage> createState() => _DeviceDropdownPageState();
}

class _DeviceDropdownPageState extends State<DeviceDropdownPage> {
  List<Device> devices = [];
  Device? selectedDevice;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchDevices();
  }

  Future<void> _fetchDevices() async {
    await Future.delayed(const Duration(seconds: 2)); // symulacja API

    setState(() {
      devices = [];
      devices = widget.deviceList;
      selectedDevice = devices.first;
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: isLoading
          ? const CircularProgressIndicator()
          : DropdownButton<Device>(
              value: selectedDevice,
              items: devices.map((device) {
                return DropdownMenuItem<Device>(
                  value: device,
                  child: Text(device.name),
                );
              }).toList(),
              onChanged: (Device? newValue) {
                setState(() {
                  selectedDevice = newValue;
                });
              },
            ),
    );
  }
}
