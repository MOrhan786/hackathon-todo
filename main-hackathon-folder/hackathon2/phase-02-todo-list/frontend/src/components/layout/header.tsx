'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { AnimatedWrapper } from '@/components/ui/animation';

interface HeaderProps {
  title: string;
  onAddNew?: () => void;
  addButtonText?: string;
  navItems?: Array<{ name: string; href: string }>;
}

const Header: React.FC<HeaderProps> = ({
  title,
  onAddNew,
  addButtonText = 'Add New',
  navItems = []
}) => {
  return (
    <AnimatedWrapper animation="fadeIn">
      <header className="sticky top-0 z-30 w-full bg-card border-b border-input">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center">
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="outline" size="icon" className="mr-4 lg:hidden">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 6h16M4 12h16M4 18h16"
                    />
                  </svg>
                </Button>
              </SheetTrigger>
              <SheetContent side="left" className="w-64 bg-card">
                <div className="flex items-center justify-center h-16 border-b border-input">
                  <h1 className="text-xl font-bold font-heading bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                    Todo App
                  </h1>
                </div>
                <nav className="mt-8">
                  <ul className="space-y-2">
                    {navItems.map((item) => (
                      <li key={item.name}>
                        <Link
                          href={item.href}
                          className="block py-2 px-4 rounded-md hover:bg-accent hover:text-accent-foreground transition-colors"
                        >
                          {item.name}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </nav>
              </SheetContent>
            </Sheet>

            <h1 className="text-2xl font-bold font-heading bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              {title}
            </h1>
          </div>

          <div className="flex items-center space-x-4">
            {onAddNew && (
              <Button onClick={onAddNew} className="hidden sm:inline-flex">
                {addButtonText}
              </Button>
            )}
            <div className="relative">
              <Button variant="ghost" size="icon" className="rounded-full">
                <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-medium">
                  U
                </div>
              </Button>
            </div>
          </div>
        </div>
      </header>
    </AnimatedWrapper>
  );
};

export default Header;