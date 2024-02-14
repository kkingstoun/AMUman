export interface Job {
    id: number; // Since readOnly is true, it might not be included in POST/PUT requests
    user?: string; // ? denotes that the property is nullable
    path?: string; // Max length of 500, nullable
    node_name?: string; // Max length of 100, nullable
    port?: number; // Integer with specified max and min values, nullable
    submit_time?: string; // Date-time string, nullable
    start_time?: string; // Date-time string, nullable
    end_time?: string; // Date-time string, nullable
    error_time?: string; // Date-time string, nullable
    priority: PriorityType; // Enum, assuming 'PriorityType' is an enum you've defined based on provided values
    gpu_partition: GpuPartitionType; // Enum, assuming 'GpuPartitionType' is an enum you've defined based on provided values
    est?: string; // Max length of 100, nullable
    status: StatusType; // Enum, assuming 'StatusType' is an enum you've defined based on provided values
    assigned_node_id?: string; // Max length of 10, nullable
    assigned_gpu_id?: string; // Max length of 10, nullable
    output?: string; // Nullable
    error?: string; // Nullable
    flags: Record<string, unknown>; // An object with an unspecified structure
}

// Example Enum Definitions (based on the 'Array [ 3 ]' and 'Array [ 5 ]' notes)
enum PriorityType {
    "Slow",
    "Normal",
    "Fast",
}

enum GpuPartitionType {
    "Slow",
    "Normal",
    "Fast",
}

enum StatusType {
    "running",
    "finished",
    "queued",
}
