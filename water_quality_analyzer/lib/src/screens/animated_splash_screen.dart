import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:math' as math;
import '../utils/constants.dart';

class AnimatedSplashScreen extends StatefulWidget {
  final Widget nextScreen;

  const AnimatedSplashScreen({
    super.key,
    required this.nextScreen,
  });

  @override
  State<AnimatedSplashScreen> createState() => _AnimatedSplashScreenState();
}

class _AnimatedSplashScreenState extends State<AnimatedSplashScreen>
    with TickerProviderStateMixin {
  late AnimationController _logoController;
  late AnimationController _rippleController;
  late Animation<double> _rippleAnimation;
  late Animation<double> _logoScaleAnimation;
  late Animation<double> _logoRotateAnimation;

  late AnimationController _textController;
  late Animation<double> _textAnimation;

  @override
  void initState() {
    super.initState();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersive);

    _logoController = AnimationController(
      duration: const Duration(milliseconds: 1800),
      vsync: this,
    );

    _rippleController = AnimationController(
      duration: const Duration(milliseconds: 1200),
      vsync: this,
    );

    _textController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );

    _rippleAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: _rippleController,
        curve: Curves.easeInOut,
      ),
    );

    _logoScaleAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: _logoController,
        curve: Curves.elasticOut,
      ),
    );

    _logoRotateAnimation = Tween<double>(begin: 0.0, end: 2 * math.pi).animate(
      CurvedAnimation(
        parent: _logoController,
        curve: const Interval(0.0, 0.6, curve: Curves.easeInOut),
      ),
    );

    _textAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: _textController,
        curve: Curves.easeInOut,
      ),
    );

    _startAnimation();
  }

  Future<void> _startAnimation() async {
    await Future.delayed(const Duration(milliseconds: 300));
    if (mounted) {
      _logoController.forward();
      await Future.delayed(const Duration(milliseconds: 800));
      if (mounted) {
        _rippleController.repeat();
        await Future.delayed(const Duration(milliseconds: 1200));
        if (mounted) {
          Navigator.pushReplacement(
            context,
            PageRouteBuilder(
              pageBuilder: (context, animation, secondaryAnimation) =>
                  FadeTransition(
                opacity: animation,
                child: widget.nextScreen,
              ),
              transitionDuration: const Duration(milliseconds: 800),
              transitionsBuilder:
                  (context, animation, secondaryAnimation, child) {
                var begin = const Offset(0.0, 0.1);
                var end = Offset.zero;
                var curve = Curves.easeOutCubic;
                var tween = Tween(begin: begin, end: end)
                    .chain(CurveTween(curve: curve));
                var offsetAnimation = animation.drive(tween);

                return SlideTransition(
                  position: offsetAnimation,
                  child: FadeTransition(
                    opacity: animation,
                    child: child,
                  ),
                );
              },
            ),
          );
        }
      }
    }
  }

  @override
  void dispose() {
    SystemChrome.setEnabledSystemUIMode(
      SystemUiMode.manual,
      overlays: SystemUiOverlay.values,
    );
    _logoController.dispose();
    _rippleController.dispose();
    _textController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Stack(
        children: [
          // Background ripple effect
          Center(
            child: AnimatedBuilder(
              animation: _rippleAnimation,
              builder: (context, child) {
                return Stack(
                  alignment: Alignment.center,
                  children: List.generate(3, (index) {
                    final delay = index * 0.3;
                    final scale = 1.0 + (_rippleAnimation.value + delay) % 1.0;
                    final opacity =
                        (1.0 - ((_rippleAnimation.value + delay) % 1.0));

                    return Transform.scale(
                      scale: scale,
                      child: Container(
                        width: 150,
                        height: 150,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: Color(0xFF3700B3).withOpacity(opacity * 0.3),
                            width: 2,
                          ),
                        ),
                      ),
                    );
                  }),
                );
              },
            ),
          ),
          // Animated logo
          Center(
            child: AnimatedBuilder(
              animation:
                  Listenable.merge([_logoScaleAnimation, _logoRotateAnimation]),
              builder: (context, child) {
                return Transform.scale(
                  scale: _logoScaleAnimation.value,
                  child: Transform.rotate(
                    angle: _logoRotateAnimation.value,
                    child: Hero(
                      tag: 'app_logo',
                      child: Image.asset(
                        AppConstants.appLogo,
                        width: 120,
                        height: 120,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          // App name with animated text reveal
          Align(
            alignment: const Alignment(0.0, 0.3),
            child: AnimatedBuilder(
              animation:
                  Listenable.merge([_logoScaleAnimation, _textAnimation]),
              builder: (context, child) {
                // Start text animation after logo animation is halfway
                if (_logoScaleAnimation.value > 0.5 &&
                    !_textController.isAnimating &&
                    !_textController.isCompleted) {
                  _textController.forward();
                }

                return Opacity(
                  opacity: _textAnimation.value,
                  child: Transform.translate(
                    offset: Offset(0, 15 * (1 - _textAnimation.value)),
                    child: ShaderMask(
                      shaderCallback: (Rect bounds) {
                        return LinearGradient(
                          colors: [
                            const Color(AppConstants.primaryColorValue),
                            const Color(AppConstants.primaryColorValue)
                                .withOpacity(0.8),
                          ],
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                        ).createShader(bounds);
                      },
                      child: Text(
                        AppConstants.appName,
                        style: Theme.of(context)
                            .textTheme
                            .headlineMedium
                            ?.copyWith(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 1.2,
                            ),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
