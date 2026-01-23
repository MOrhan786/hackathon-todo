import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AnimatedWrapper } from '@/components/ui/animation';

interface ErrorStateProps {
  title: string;
  description: string;
  onRetry?: () => void;
  errorIcon?: React.ReactNode;
  className?: string;
}

const ErrorState: React.FC<ErrorStateProps> = ({
  title,
  description,
  onRetry,
  errorIcon,
  className
}) => {
  return (
    <AnimatedWrapper animation="fadeIn" className={className}>
      <Card className="flex flex-col items-center justify-center p-12 text-center">
        <div className="mb-4 text-red-400">
          {errorIcon || (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-16 w-16 mx-auto"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          )}
        </div>
        <h3 className="text-xl font-semibold text-foreground mb-2">{title}</h3>
        <p className="text-muted-foreground mb-6">{description}</p>
        {onRetry && (
          <Button variant="outline" onClick={onRetry}>
            Try Again
          </Button>
        )}
      </Card>
    </AnimatedWrapper>
  );
};

export default ErrorState;