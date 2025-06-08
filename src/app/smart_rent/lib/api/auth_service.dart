import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:smart_rent/api/config.dart';

class AuthService {
  final String baseUrl = service1; // Android emulator

  Future<Map<String, dynamic>> register(
      String email, String password, String name) async {
    final response = await http.post(
      Uri.parse('$baseUrl/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
        'name': name,
      }),
    );

    if (response.statusCode == 201) {
      return {'success': true, 'message': 'User registered successfully'};
    } else {
      return {
        'success': false,
        ...jsonDecode(response.body),
      };
    }
  }

  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return {
        'success': true,
        'access_token': data['access_token'],
        'user_id': data['user_id'],
      };
    } else {
      return {
        'success': false,
        ...jsonDecode(response.body),
      };
    }
  }
}

class AuthProvider extends ChangeNotifier {
  String _token = '';
  int? _userId;

  String get token => _token;
  int? get userId => _userId;

  void setAuthData(String token, int userId) {
    _token = token;
    _userId = userId;
    notifyListeners();
  }

  void clearAuth() {
    _token = '';
    _userId = null;
    notifyListeners();
  }
}
