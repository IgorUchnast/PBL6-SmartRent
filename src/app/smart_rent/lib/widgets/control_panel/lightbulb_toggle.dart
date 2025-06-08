import 'package:flutter/material.dart';
import 'package:smart_rent/api/lightbulb.dart';
import 'package:smart_rent/api/lightbulb_service.dart';

class LightbulbToggle extends StatefulWidget {
  final int lightbulbId;

  const LightbulbToggle({super.key, required this.lightbulbId});

  @override
  State<LightbulbToggle> createState() => _LightbulbToggleState();
}

class _LightbulbToggleState extends State<LightbulbToggle> {
  Lightbulb? _lightbulb;
  bool _isLoading = true;

  final List<String> _states = ['off', 'on', 'auto'];

  @override
  void initState() {
    super.initState();
    _loadLightbulb();
  }

  Future<void> _loadLightbulb() async {
    try {
      final bulb = await fetchLightbulb(widget.lightbulbId);
      setState(() {
        _lightbulb = bulb;
        _isLoading = false;
      });
    } catch (_) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _cycleStatus() async {
    if (_lightbulb == null) return;

    final currentIndex = _states.indexOf(_lightbulb!.status);
    final nextIndex = (currentIndex + 1) % _states.length;
    final newStatus = _states[nextIndex];

    try {
      await updateLightbulbStatus(widget.lightbulbId, newStatus);
      setState(() {
        _lightbulb!.status = newStatus;
      });
    } catch (_) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Błąd zmiany stanu')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) return const CircularProgressIndicator();

    IconData icon;
    Color color;
    String label;

    switch (_lightbulb!.status) {
      case 'on':
        icon = Icons.lightbulb;
        color = Colors.yellow;
        label = 'Auto';
        break;
      case 'auto':
        icon = Icons.bolt;
        color = Colors.blueAccent;
        label = 'OFF';
        break;
      case 'off':
      default:
        icon = Icons.lightbulb_outline;
        color = Colors.grey;
        label = 'ON';
        break;
    }

    return Column(
      children: [
        Icon(icon, size: 60, color: color),
        const SizedBox(height: 10),
        ElevatedButton(
          onPressed: _cycleStatus,
          child: Text(label),
        ),
      ],
    );
  }
}
