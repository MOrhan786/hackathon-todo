import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

interface NavItem {
  name: string;
  href: string;
  icon: React.ReactNode;
}

interface ResponsiveNavigationProps {
  items: NavItem[];
  activeItem: string;
  className?: string;
}

const ResponsiveNavigation: React.FC<ResponsiveNavigationProps> = ({
  items,
  activeItem,
  className = ''
}) => {
  return (
    <nav className={`bg-card border-t border-input md:hidden fixed bottom-0 left-0 right-0 z-40 ${className}`}>
      <div className="flex justify-around items-center h-16 px-2">
        {items.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className={`flex flex-col items-center justify-center h-full w-full py-2 ${
              activeItem === item.name
                ? 'text-primary'
                : 'text-foreground/60 hover:text-foreground'
            }`}
          >
            <span className="mb-1">{item.icon}</span>
            <span className="text-xs font-medium">{item.name}</span>
          </Link>
        ))}
      </div>
    </nav>
  );
};

export default ResponsiveNavigation;