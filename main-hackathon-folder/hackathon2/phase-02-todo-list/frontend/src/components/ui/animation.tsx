'use client';

import { motion } from 'framer-motion';

// Fade in animation
export const FadeIn = motion.div;

// Slide in from left
export const SlideInLeft = motion.div;

// Slide in from right
export const SlideInRight = motion.div;

// Slide in from top
export const SlideInTop = motion.div;

// Slide in from bottom
export const SlideInBottom = motion.div;

// Scale in animation
export const ScaleIn = motion.div;

// Bounce animation
export const Bounce = motion.div;

// Common animation presets
export const fadeInVariant = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.3 } },
};

export const slideInLeftVariant = {
  hidden: { x: -100, opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { duration: 0.3 } },
};

export const slideInRightVariant = {
  hidden: { x: 100, opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { duration: 0.3 } },
};

export const slideInTopVariant = {
  hidden: { y: -100, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { duration: 0.3 } },
};

export const slideInBottomVariant = {
  hidden: { y: 100, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { duration: 0.3 } },
};

export const scaleInVariant = {
  hidden: { scale: 0.8, opacity: 0 },
  visible: { scale: 1, opacity: 1, transition: { duration: 0.3 } },
};

export const bounceVariant = {
  hidden: { y: 100, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      type: 'spring',
      stiffness: 300,
      damping: 20
    }
  },
};

// Animation wrapper component
interface AnimatedWrapperProps {
  children: React.ReactNode;
  animation?: 'fadeIn' | 'slideInLeft' | 'slideInRight' | 'slideInTop' | 'slideInBottom' | 'scaleIn' | 'bounce';
  delay?: number;
  duration?: number;
  className?: string;
}

export const AnimatedWrapper: React.FC<AnimatedWrapperProps> = ({
  children,
  animation = 'fadeIn',
  delay = 0,
  duration = 0.3,
  className
}) => {
  const variantsMap: Record<string, any> = {
    fadeIn: fadeInVariant,
    slideInLeft: slideInLeftVariant,
    slideInRight: slideInRightVariant,
    slideInTop: slideInTopVariant,
    slideInBottom: slideInBottomVariant,
    scaleIn: scaleInVariant,
    bounce: bounceVariant,
  };

  const MotionComponent = motion.div;

  return (
    <MotionComponent
      initial="hidden"
      animate="visible"
      variants={variantsMap[animation]}
      transition={{ duration, delay }}
      className={className}
    >
      {children}
    </MotionComponent>
  );
};