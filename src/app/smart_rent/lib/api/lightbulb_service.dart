import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:smart_rent/api/config.dart';
import 'lightbulb.dart';

// Zmienione URL na report_service
const String baseUrl = '$service2/api';

Future<Lightbulb> fetchLightbulb(int id) async {
  final response = await http.get(Uri.parse('$baseUrl/lightbulbs/$id'));
  if (response.statusCode == 200) {
    return Lightbulb.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to fetch lightbulb');
  }
}

Future<void> updateLightbulbStatus(int id, String status) async {
  final response = await http.patch(
    Uri.parse('$baseUrl/lightbulbs/$id'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'status': status}),
  );
  if (response.statusCode != 200) {
    throw Exception('Failed to update lightbulb status');
  }
}
