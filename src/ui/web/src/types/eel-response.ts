export interface EelResponse<TData> {
    data: TData | null
    error: {
        name: string
        explanation: string
    }
}