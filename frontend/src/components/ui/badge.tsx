import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

// Badge variant definitions using CVA
const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
        secondary:
          'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
        destructive:
          'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',
        outline: 'text-foreground hover:bg-accent border-input',
        success: 'border-transparent bg-success text-success-foreground hover:bg-success/80',
        warning: 'border-transparent bg-accent text-accent-foreground hover:bg-accent/80',
        info: 'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
        pending: 'border-transparent bg-muted text-muted-foreground hover:bg-muted/80',
        // Priority variants matching the design spec
        high: 'border-transparent bg-destructive text-destructive-foreground', // Red for high priority
        medium: 'border-transparent bg-accent text-accent-foreground', // Purple for medium priority
        low: 'border-transparent bg-success text-success-foreground', // Green for low priority
        // Status variants
        completed: 'border-transparent bg-success text-success-foreground',
        overdue: 'border-transparent bg-destructive text-destructive-foreground',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

// Badge props interface
export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

// Badge component implementation
function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };