import 'package:flutter/material.dart';
import '../widgets/custom_app_bar.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final _nameController = TextEditingController(text: 'Dr. John Doe');
  final _emailController = TextEditingController(text: 'john.doe@example.com');
  bool _isEditingMode = false;

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    super.dispose();
  }

  Widget _buildStatColumn(String value, String label) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 14,
            color: Colors.white.withOpacity(0.8),
          ),
        ),
      ],
    );
  }

  Widget _buildMenuItem({
    required IconData icon,
    required String title,
    Widget? trailing,
    Color? textColor,
    required VoidCallback onTap,
  }) {
    return ListTile(
      leading: Icon(
        icon,
        color: textColor ?? Colors.grey[700],
      ),
      title: Text(
        title,
        style: TextStyle(
          color: textColor ?? Colors.grey[900],
          fontWeight: FontWeight.w500,
        ),
      ),
      trailing: trailing ?? const Icon(Icons.chevron_right, color: Colors.grey),
      onTap: onTap,
    );
  }

  Widget _buildSection({
    required String title,
    required List<Widget> items,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text(
            title,
            style: TextStyle(
              color: Colors.grey[600],
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
        ...items,
        const SizedBox(height: 16),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'Profile',
        showBackButton: false,
        additionalActions: [
          IconButton(
            icon: const Icon(Icons.edit_outlined),
            onPressed: () {
              // Enable editing mode
              setState(() {
                _isEditingMode = true;
              });
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.symmetric(vertical: 32),
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Color(0xFF3900B3),
                    Color(0xFF5C1BDB),
                  ],
                ),
              ),
              child: Column(
                children: [
                  Stack(
                    children: [
                      CircleAvatar(
                        radius: 50,
                        backgroundColor: Colors.white,
                        child: Icon(
                          Icons.person,
                          size: 50,
                          color: const Color(0xFF3900B3).withOpacity(0.7),
                        ),
                      ),
                      if (_isEditingMode)
                        Positioned(
                          bottom: 0,
                          right: 0,
                          child: Container(
                            padding: const EdgeInsets.all(4),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              shape: BoxShape.circle,
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.1),
                                  blurRadius: 4,
                                  offset: const Offset(0, 2),
                                ),
                              ],
                            ),
                            child: const Icon(
                              Icons.camera_alt,
                              size: 16,
                              color: Color(0xFF3900B3),
                            ),
                          ),
                        ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  _isEditingMode
                      ? TextFormField(
                          controller: _nameController,
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                          ),
                          decoration: const InputDecoration(
                            border: InputBorder.none,
                            contentPadding: EdgeInsets.zero,
                          ),
                        )
                      : Text(
                          _nameController.text,
                          style: const TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                  const SizedBox(height: 8),
                  _isEditingMode
                      ? TextFormField(
                          controller: _emailController,
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.white.withOpacity(0.8),
                          ),
                          decoration: const InputDecoration(
                            border: InputBorder.none,
                            contentPadding: EdgeInsets.zero,
                          ),
                        )
                      : Text(
                          'Water Quality Specialist',
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.white.withOpacity(0.8),
                          ),
                        ),
                  const SizedBox(height: 24),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildStatColumn('124', 'Samples'),
                      Container(
                        width: 1,
                        height: 40,
                        color: Colors.white.withOpacity(0.2),
                      ),
                      _buildStatColumn('45', 'Reports'),
                      Container(
                        width: 1,
                        height: 40,
                        color: Colors.white.withOpacity(0.2),
                      ),
                      _buildStatColumn('4.8', 'Rating'),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            _buildSection(
              title: 'Account',
              items: [
                _buildMenuItem(
                  icon: Icons.person_outline,
                  title: 'Personal Information',
                  onTap: () {},
                ),
                _buildMenuItem(
                  icon: Icons.notifications_outlined,
                  title: 'Notifications',
                  trailing: Switch(
                    value: true,
                    activeColor: const Color(0xFF3900B3),
                    onChanged: (value) {},
                  ),
                  onTap: () {}, // Add this line
                ),
                _buildMenuItem(
                  icon: Icons.privacy_tip_outlined,
                  title: 'Privacy Settings',
                  onTap: () {},
                ),
              ],
            ),
            _buildSection(
              title: 'Activity',
              items: [
                _buildMenuItem(
                  icon: Icons.history,
                  title: 'Sample History',
                  onTap: () {},
                ),
                _buildMenuItem(
                  icon: Icons.analytics_outlined,
                  title: 'Analytics',
                  onTap: () {},
                ),
                _buildMenuItem(
                  icon: Icons.star_outline,
                  title: 'Achievements',
                  trailing: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFF3900B3).withOpacity(0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text(
                      'NEW',
                      style: TextStyle(
                        color: Color(0xFF3900B3),
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  onTap: () {},
                ),
              ],
            ),
            _buildSection(
              title: 'Support',
              items: [
                _buildMenuItem(
                  icon: Icons.help_outline,
                  title: 'Help & Support',
                  onTap: () {},
                ),
                _buildMenuItem(
                  icon: Icons.info_outline,
                  title: 'About App',
                  onTap: () {},
                ),
                _buildMenuItem(
                  icon: Icons.logout,
                  title: 'Logout',
                  textColor: Colors.red,
                  onTap: () =>
                      Navigator.of(context).pushReplacementNamed('/auth'),
                ),
              ],
            ),
            const SizedBox(height: 24),
            Text(
              'Version 1.0.0',
              style: TextStyle(
                color: Colors.grey[600],
                fontSize: 12,
              ),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }
}
