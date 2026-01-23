import React from 'react';
import { Badge } from '@/components/ui/badge';

interface StatusIndicatorProps {
  status: 'pending' | 'in-progress' | 'completed' | 'overdue' | 'cancelled';
  className?: string;
}

const StatusIndicator: React.FC<StatusIndicatorProps> = ({ status, className }) => {
  const getStatusVariant = () => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'overdue':
        return 'destructive';
      case 'in-progress':
        return 'warning';
      case 'cancelled':
        return 'outline';
      case 'pending':
      default:
        return 'pending';
    }
  };

  const getStatusText = (): string => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'overdue':
        return 'Overdue';
      case 'in-progress':
        return 'In Progress';
      case 'cancelled':
        return 'Cancelled';
      case 'pending':
        return 'Pending';
    }
  };

  return (
    <Badge variant={getStatusVariant()} className={className}>
      {getStatusText()}
    </Badge>
  );
};

export default StatusIndicator;