import React from 'react';
import { cn } from '@/lib/utils';

interface SkeletonProps {
  className?: string;
  count?: number;
  variant?: 'card' | 'list-item' | 'text' | 'avatar' | 'button';
}

const Skeleton: React.FC<SkeletonProps> = ({
  className = '',
  count = 1,
  variant = 'text'
}) => {
  const baseClasses = "animate-pulse rounded-md bg-muted";

  const variantClasses = {
    card: "h-32 w-full",
    'list-item': "h-16 w-full",
    text: "h-4 w-full",
    avatar: "h-10 w-10 rounded-full",
    button: "h-10 w-24 rounded-md",
  };

  const skeletons = Array.from({ length: count }).map((_, index) => (
    <div
      key={index}
      className={cn(baseClasses, variantClasses[variant], className)}
    />
  ));

  return <>{skeletons}</>;
};

export default Skeleton;