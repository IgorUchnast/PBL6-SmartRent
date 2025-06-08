// import 'dart:convert';

// import 'package:http/http.dart' as http;

// Future<Map<String, dynamic>> addProperty(
//     String token, String description, double price,
//     {String status = 'free'}) async {
//   final response = await http.post(
//     Uri.parse('http://localhost:8002/api/properties'),
//     headers: {
//       'Content-Type': 'application/json',
//       'Authorization': 'Bearer $token',
//     },
//     body: jsonEncode({
//       'description': description,
//       'price': price,
//       'status': status,
//     }),
//   );

//   return jsonDecode(response.body);
// }

import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:smart_rent/api/config.dart';

Future<Map<String, dynamic>> addProperty(
  String token,
  String description,
  double price,
  String status,
  String adress,
) async {
  final response = await http.post(
    Uri.parse("$service2/api/properties"),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    },
    body: jsonEncode({
      'description': description,
      'price': price,
      'status': status,
      'adress': adress,
    }),
  );

  return jsonDecode(response.body);
}
