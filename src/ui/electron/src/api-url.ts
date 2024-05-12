import { ApiResponse } from '@/types/api-response'

export const API_BASE_URL = 'http://127.0.0.1:5000'

export async function fetchApi<TData = any>(path: string,
    fetchOptions?: RequestInit): Promise<ApiResponse<TData>> {

    const responseData = await (await fetch(path, fetchOptions)).json()

    

    return responseData
}
