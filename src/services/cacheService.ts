interface CacheItem<T> {
    data: T;
    timestamp: number;
}

export class Cache<T> {
    private cache: Map<string, CacheItem<T>> = new Map();
    private ttl: number;

    constructor(ttlSeconds: number) {
        this.ttl = ttlSeconds * 1000; // Convert to milliseconds
    }

    set(key: string, value: T): void {
        this.cache.set(key, {
            data: value,
            timestamp: Date.now()
        });
    }

    get(key: string): T | undefined {
        const item = this.cache.get(key);
        if (!item) return undefined;

        if (Date.now() - item.timestamp > this.ttl) {
            this.cache.delete(key);
            return undefined;
        }

        return item.data;
    }

    clear(): void {
        this.cache.clear();
    }
}
