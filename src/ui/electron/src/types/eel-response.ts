export interface EelResponse<TData = null> {
    data: TData | null
    error: {
        name: string
        explanation: string
    } | null
}