'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground overflow-hidden">
      {/* Navigation */}
      <header className="relative z-10 flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
          <span className="text-xl font-bold font-heading">TodoAI</span>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/login">
            <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
              Sign In
            </Button>
          </Link>
          <Link href="/signup">
            <Button variant="gradient" size="sm">
              Get Started
            </Button>
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative px-6 pt-16 pb-24 max-w-7xl mx-auto text-center">
        {/* Decorative orbs */}
        <div className="absolute top-0 left-1/4 w-72 h-72 bg-primary/20 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute top-20 right-1/4 w-64 h-64 bg-accent/20 rounded-full blur-[120px] pointer-events-none" />

        <div className="relative z-10 animate-fade-in">
          <div className="inline-block mb-6 px-4 py-1.5 rounded-full border border-primary/30 bg-primary/10 text-primary text-sm font-medium">
            AI-Powered Task Management
          </div>
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold font-heading leading-tight mb-6">
            Organize your life
            <br />
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              with intelligence
            </span>
          </h1>
          <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            Create tasks, set reminders, and chat with an AI assistant that helps you stay productive. The smartest way to manage your todos.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/signup">
              <Button variant="gradient" size="lg" className="text-base px-8">
                Get Started Free
              </Button>
            </Link>
            <Link href="/login">
              <Button variant="outline" size="lg" className="text-base px-8">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-20 max-w-7xl mx-auto">
        <div className="text-center mb-14 animate-fade-in">
          <h2 className="text-3xl sm:text-4xl font-bold font-heading mb-4">
            Everything you need to stay on track
          </h2>
          <p className="text-muted-foreground text-lg max-w-xl mx-auto">
            Powerful features designed to boost your productivity and keep you organized.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="border-primary/10 bg-card/50 backdrop-blur animate-slide-up">
            <CardHeader>
              <div className="h-12 w-12 rounded-xl bg-primary/10 flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <CardTitle className="text-xl">Smart Tasks</CardTitle>
              <CardDescription className="text-base">
                Create, organize, and prioritize your tasks with an intuitive interface. Set due dates and track progress effortlessly.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-accent/10 bg-card/50 backdrop-blur animate-slide-up [animation-delay:100ms]">
            <CardHeader>
              <div className="h-12 w-12 rounded-xl bg-accent/10 flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <CardTitle className="text-xl">AI Chat Assistant</CardTitle>
              <CardDescription className="text-base">
                Chat with an AI that understands your tasks. Get suggestions, create tasks through conversation, and stay motivated.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-success/10 bg-card/50 backdrop-blur animate-slide-up [animation-delay:200ms]">
            <CardHeader>
              <div className="h-12 w-12 rounded-xl bg-success/10 flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <CardTitle className="text-xl">Smart Reminders</CardTitle>
              <CardDescription className="text-base">
                Never miss a deadline. Set intelligent reminders that keep you on track and help you manage your time effectively.
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* How It Works */}
      <section className="px-6 py-20 max-w-7xl mx-auto">
        <div className="text-center mb-14">
          <h2 className="text-3xl sm:text-4xl font-bold font-heading mb-4">
            How it works
          </h2>
          <p className="text-muted-foreground text-lg max-w-xl mx-auto">
            Get started in seconds and take control of your productivity.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { step: '1', title: 'Create', desc: 'Add tasks with details, priorities, and due dates in seconds.' },
            { step: '2', title: 'Organize', desc: 'Sort, filter, and manage your tasks with powerful tools.' },
            { step: '3', title: 'Complete', desc: 'Track your progress and celebrate as you check things off.' },
          ].map((item) => (
            <div key={item.step} className="text-center">
              <div className="mx-auto mb-4 h-14 w-14 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white text-xl font-bold font-heading">
                {item.step}
              </div>
              <h3 className="text-xl font-semibold font-heading mb-2">{item.title}</h3>
              <p className="text-muted-foreground">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20 max-w-7xl mx-auto">
        <div className="relative rounded-2xl border border-primary/20 bg-card/50 backdrop-blur p-12 text-center overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-accent/5 pointer-events-none" />
          <div className="relative z-10">
            <h2 className="text-3xl sm:text-4xl font-bold font-heading mb-4">
              Ready to get organized?
            </h2>
            <p className="text-muted-foreground text-lg max-w-lg mx-auto mb-8">
              Join and start managing your tasks with the power of AI. Free to get started.
            </p>
            <Link href="/signup">
              <Button variant="gradient" size="lg" className="text-base px-10">
                Start Now
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-8 max-w-7xl mx-auto border-t border-input">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <div className="h-6 w-6 rounded bg-gradient-to-br from-primary to-accent flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <span className="font-heading font-semibold text-foreground">TodoAI</span>
          </div>
          <p>&copy; {new Date().getFullYear()} TodoAI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
