// API Error Types

export interface APIError {
  status: number;
  message: string;
  detail?: string;
}

export interface FieldError {
  field: string;
  message: string;
}

export interface ValidationError extends APIError {
  status: 422;
  errors: FieldError[];
}
