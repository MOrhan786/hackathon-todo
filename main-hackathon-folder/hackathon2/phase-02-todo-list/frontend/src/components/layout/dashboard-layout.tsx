'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { AnimatedWrapper } from '@/components/ui/animation';
import Link from 'next/link';

interface DashboardLayoutProps {
  children: React.ReactNode;
  title?: string;
  onAddNew?: () => void;
  addButtonText?: string;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  title = 'Dashboard',
  onAddNew,
  addButtonText = 'Add New'
}) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navItems = [
    { name: 'Dashboard', href: '/' },
    { name: 'Tasks', href: '/tasks' },
    { name: 'Calendar', href: '/calendar' },
    { name: 'Settings', href: '/settings' },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile sidebar */}
      <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
        <SheetTrigger asChild>
          <Button
            variant="outline"
            size="icon"
            className="fixed top-4 left-4 z-50 md:hidden"
          >
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
                    onClick={() => setSidebarOpen(false)}
                  >
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </SheetContent>
      </Sheet>

      {/* Desktop sidebar */}
      <aside className="fixed inset-y-0 left-0 z-40 w-64 bg-card border-r border-input hidden lg:block">
        <div className="flex items-center justify-center h-16 border-b border-input">
          <h1 className="text-xl font-bold font-heading bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            Todo App
          </h1>
        </div>
        <nav className="mt-8 px-4">
          <ul className="space-y-2">
            {navItems.map((item) => (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className="flex items-center py-2 px-4 rounded-md hover:bg-accent hover:text-accent-foreground transition-colors"
                >
                  {item.name}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      {/* Main content */}
      <main className="lg:ml-64 pb-24 md:pb-16">
        <header className="sticky top-0 z-30 bg-card border-b border-input">
          <div className="container mx-auto px-4 py-4 flex items-center justify-between">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold font-heading bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                {title}
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              {onAddNew && (
                <Button onClick={onAddNew}>
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

        <AnimatedWrapper animation="fadeIn" className="container mx-auto px-4 py-8 max-w-7xl">
          {children}
        </AnimatedWrapper>
      </main>
    </div>
  );
};

export default DashboardLayout;