export type ApiResponse<TData = any> = {
    error: {
        code: number
        explanation: string
    } | null
    data: TData | null
}
