import { useNotificationsStore } from '@/stores/notifications'
import { API_BASE_URL } from '@/api-url'
import { ApiResponse } from '@/types/api-response'

export function useApi() {
    const { showNotification } = useNotificationsStore()

    async function fetchWithErrorNotification<TData = any>(
        path: string,
        options?: RequestInit,
        errorTextBeginning: string = 'error: ',
    ) {
        const response = await fetch(API_BASE_URL + path, {
            headers: {
                'Content-Type': 'application/json'
            },
            ...options
        })
        
        const responseData: ApiResponse<TData> = await response.json()

        if(responseData.error) {
            showNotification({
                type: 'error',
                text: `${errorTextBeginning} '${responseData.error.explanation}'`
            })
        }

        return responseData
    }

    return { fetchWithErrorNotification }
}
