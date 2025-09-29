import 'package:flutter/material.dart';
import 'home_screen.dart';
import 'statistics_screen.dart';
import 'data_input_screen.dart';
import 'educational_modules_screen.dart';
import 'profile_screen.dart';
import 'chatbot_screen.dart';
import '../widgets/custom_bottom_nav_bar.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const HomeScreen(),
    const StatisticsScreen(),
    const DataInputScreen(),
    const EducationalModulesScreen(),
    const ProfileScreen(),
  ];

  void _onItemTapped(int index) {
    if (index == 2) {
      // Index 2 is the chatbot button
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (context) => const ChatbotScreen(),
        ),
      );
    } else {
      setState(() {
        _selectedIndex = index;
      });
    }
  }

  void _openInputScreen() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => const DataInputScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      floatingActionButton: Padding(
        padding: const EdgeInsets.only(bottom: 20.0),
        child: FloatingActionButton(
          onPressed: _openInputScreen,
          backgroundColor: const Color(0xFF3700B3),
          child: const Icon(
            Icons.add,
            color: Colors.white,
          ),
        ),
      ),
      bottomNavigationBar: CustomBottomNavBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
      ),
    );
  }
}
