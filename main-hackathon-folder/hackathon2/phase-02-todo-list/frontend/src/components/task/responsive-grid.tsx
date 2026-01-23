import React from 'react';
import { cn } from '@/lib/utils';

interface ResponsiveGridProps {
  children: React.ReactNode;
  className?: string;
  cols?: {
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
  };
}

const ResponsiveGrid: React.FC<ResponsiveGridProps> = ({
  children,
  className = '',
  cols = { sm: 1, md: 2, lg: 3, xl: 4 }
}) => {
  const gridColsClass = `grid-cols-${cols.sm} sm:grid-cols-${cols.sm} md:grid-cols-${cols.md} lg:grid-cols-${cols.lg} xl:grid-cols-${cols.xl}`;

  return (
    <div className={cn(`grid gap-4 ${gridColsClass}`, className)}>
      {children}
    </div>
  );
};

export default ResponsiveGrid;