import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:smart_rent/api/auth_service.dart';
// import 'package:smart_rent/pages/login_page.dart';
import 'package:smart_rent/pages/resgister_page.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(),
      home: RegisterPage(),
    );
  }
}
