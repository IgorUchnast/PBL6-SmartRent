import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:smart_rent/api/auth_service.dart';
import 'package:smart_rent/pages/home_page.dart';

enum LoginStatus { idle, loading, success, error }

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final AuthService _authService = AuthService();
  LoginStatus _loginStatus = LoginStatus.idle;

  void _login(BuildContext context) async {
    setState(() {
      _loginStatus = LoginStatus.loading;
    });

    final result = await _authService.login(
      _emailController.text.trim(),
      _passwordController.text.trim(),
    );

    if (result['success'] == true &&
        result['access_token'] != null &&
        result['user_id'] != null) {
      // ✅ Zapisz token i userId do providera
      Provider.of<AuthProvider>(context, listen: false)
          .setAuthData(result['access_token'], result['user_id']);

      setState(() => _loginStatus = LoginStatus.success);

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Zalogowano!')),
      );

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const HomePage()),
      );
    } else {
      setState(() => _loginStatus = LoginStatus.error);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(result['error'] ?? 'Błąd logowania')),
      );
    }

    setState(() {
      _loginStatus = LoginStatus.idle;
    });
  }

  @override
  Widget build(BuildContext context) {
    final isLoading = _loginStatus == LoginStatus.loading;

    return Scaffold(
      appBar: AppBar(title: const Text("Logowanie")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'Email'),
            ),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: const InputDecoration(labelText: 'Hasło'),
            ),
            const SizedBox(height: 20),
            isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: () => _login(context),
                    child: const Text("Zaloguj się"),
                  ),
          ],
        ),
      ),
    );
  }
}
