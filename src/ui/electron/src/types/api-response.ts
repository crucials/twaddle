export type ApiResponse<TData = any> = TData | { error: number, explanation: string }
