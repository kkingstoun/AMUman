/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export interface AuthUser {
	readonly id: number;
	/** @maxLength 128 */
	password: string;
	/** @format date-time */
	last_login?: string | null;
	/**
	 * Superuser status
	 * Designates that this user has all permissions without explicitly assigning them.
	 */
	is_superuser?: boolean;
	/**
	 * Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
	 * @maxLength 150
	 * @pattern ^[\w.@+-]+$
	 */
	username: string;
	/** @maxLength 150 */
	first_name?: string;
	/** @maxLength 150 */
	last_name?: string;
	/**
	 * Email address
	 * @format email
	 * @maxLength 254
	 */
	email?: string;
	/**
	 * Staff status
	 * Designates whether the user can log into this admin site.
	 */
	is_staff?: boolean;
	/**
	 * Active
	 * Designates whether this user should be treated as active. Unselect this instead of deleting accounts.
	 */
	is_active?: boolean;
	/** @format date-time */
	date_joined?: string;
	/** The groups this user belongs to. A user will get all permissions granted to each of their groups. */
	groups?: number[];
	/** Specific permissions for this user. */
	user_permissions?: number[];
}

/**
 * * `CONNECTED` - CONNECTED
 * * `DISCONNECTED` - DISCONNECTED
 */
export enum ConnectionStatusEnum {
	CONNECTED = 'CONNECTED',
	DISCONNECTED = 'DISCONNECTED'
}

export interface CustomUser {
	username: string;
	password: string;
	/** @format email */
	email: string;
	readonly concurrent_jobs: number;
	readonly auth: AuthUser;
}

export interface Gpu {
	readonly id: number;
	/** The associated node ID. */
	node: number;
	/**
	 * The unique device identifier (must be <= 32767).
	 * @format int64
	 * @min 0
	 * @max 32767
	 */
	device_id: number;
	/**
	 * The unique identifier of the GPU.
	 * @format uuid
	 */
	uuid: string;
	model: string;
	/**
	 * * `SLOW` - SLOW
	 * * `NORMAL` - NORMAL
	 * * `FAST` - FAST
	 */
	speed?: SpeedEnum;
	/**
	 * The utilization of the GPU (must be <= 100).
	 * @format int64
	 * @min 0
	 * @max 100
	 */
	util: number;
	is_running_amumax?: boolean;
	/**
	 * * `RUNNING` - RUNNING
	 * * `PENDING` - PENDING
	 * * `RESERVED` - RESERVED
	 * * `UNAVAILABLE` - UNAVAILABLE
	 */
	status?: GpuStatusEnum;
	/**
	 * The timestamp of the last update (read-only, auto-generated).
	 * @format date-time
	 */
	readonly last_update: string;
}

/**
 * * `SLOW` - SLOW
 * * `NORMAL` - NORMAL
 * * `FAST` - FAST
 * * `UNDEF` - UNDEF
 */
export enum GpuPartitionEnum {
	SLOW = 'SLOW',
	NORMAL = 'NORMAL',
	FAST = 'FAST',
	UNDEF = 'UNDEF'
}

/**
 * * `RUNNING` - RUNNING
 * * `PENDING` - PENDING
 * * `RESERVED` - RESERVED
 * * `UNAVAILABLE` - UNAVAILABLE
 */
export enum GpuStatusEnum {
	RUNNING = 'RUNNING',
	PENDING = 'PENDING',
	RESERVED = 'RESERVED',
	UNAVAILABLE = 'UNAVAILABLE'
}

export interface Job {
	readonly id: number;
	/** @maxLength 500 */
	path: string;
	/** @maxLength 150 */
	user: string;
	/**
	 * @format int64
	 * @min 0
	 * @max 9223372036854776000
	 */
	port?: number | null;
	/** @format date-time */
	submit_time?: string | null;
	/** @format date-time */
	start_time?: string | null;
	/** @format date-time */
	end_time?: string | null;
	/** @format date-time */
	error_time?: string | null;
	/**
	 * * `LOW` - LOW
	 * * `NORMAL` - NORMAL
	 * * `HIGH` - HIGH
	 */
	priority?: PriorityEnum;
	/**
	 * * `SLOW` - SLOW
	 * * `NORMAL` - NORMAL
	 * * `FAST` - FAST
	 * * `UNDEF` - UNDEF
	 */
	gpu_partition?: GpuPartitionEnum;
	/**
	 * @format int64
	 * @min 0
	 * @max 9223372036854776000
	 */
	duration?: number;
	/**
	 * * `PENDING` - PENDING
	 * * `FINISHED` - FINISHED
	 * * `INTERRUPTED` - INTERRUPTED
	 * * `RUNNING` - RUNNING
	 */
	status?: JobStatusEnum;
	output?: string | null;
	error?: string | null;
	/** @maxLength 150 */
	flags?: string | null;
	node?: number | null;
	gpu?: number | null;
}

/**
 * * `PENDING` - PENDING
 * * `FINISHED` - FINISHED
 * * `INTERRUPTED` - INTERRUPTED
 * * `RUNNING` - RUNNING
 */
export enum JobStatusEnum {
	PENDING = 'PENDING',
	FINISHED = 'FINISHED',
	INTERRUPTED = 'INTERRUPTED',
	RUNNING = 'RUNNING'
}

export interface Node {
	readonly id: number;
	ip: string;
	/** @maxLength 15 */
	name: string;
	/**
	 * @format int64
	 * @min 0
	 * @max 9223372036854776000
	 */
	number_of_gpus: number;
	/**
	 * * `PENDING` - PENDING
	 * * `RESERVED` - RESERVED
	 * * `UNAVAILABLE` - UNAVAILABLE
	 */
	status?: NodeStatusEnum;
	/**
	 * * `CONNECTED` - CONNECTED
	 * * `DISCONNECTED` - DISCONNECTED
	 */
	connection_status?: ConnectionStatusEnum;
	/** @format date-time */
	last_seen?: string;
}

/**
 * * `PENDING` - PENDING
 * * `RESERVED` - RESERVED
 * * `UNAVAILABLE` - UNAVAILABLE
 */
export enum NodeStatusEnum {
	PENDING = 'PENDING',
	RESERVED = 'RESERVED',
	UNAVAILABLE = 'UNAVAILABLE'
}

export interface PaginatedCustomUserList {
	/** @example 123 */
	count?: number;
	/**
	 * @format uri
	 * @example "http://api.example.org/accounts/?offset=400&limit=100"
	 */
	next?: string | null;
	/**
	 * @format uri
	 * @example "http://api.example.org/accounts/?offset=200&limit=100"
	 */
	previous?: string | null;
	results?: CustomUser[];
}

export interface PaginatedGpuList {
	/** @example 123 */
	count?: number;
	/**
	 * @format uri
	 * @example "http://api.example.org/accounts/?offset=400&limit=100"
	 */
	next?: string | null;
	/**
	 * @format uri
	 * @example "http://api.example.org/accounts/?offset=200&limit=100"
	 */
	previous?: string | null;
	results?: Gpu[];
}

export interface PaginatedJobList {
	/** @example 123 */
	count?: number;
	/**
	 * @format uri
	 * @example "http://api.example.org/accounts/?offset=400&limit=100"
	 */
	next?: string | null;
	/**
	 * @format uri
	 * @example "http://api.example.org/accounts/?offset=200&limit=100"
	 */
	previous?: string | null;
	results?: Job[];
}

export interface PaginatedNodeList {
	/** @example 123 */
	count?: number;
	/**
	 * @format uri
	 * @example "http://api.example.org/accounts/?offset=400&limit=100"
	 */
	next?: string | null;
	/**
	 * @format uri
	 * @example "http://api.example.org/accounts/?offset=200&limit=100"
	 */
	previous?: string | null;
	results?: Node[];
}

export interface PatchedCustomUser {
	username?: string;
	password?: string;
	/** @format email */
	email?: string;
	readonly concurrent_jobs?: number;
	readonly auth?: AuthUser;
}

export interface PatchedJob {
	readonly id?: number;
	/** @maxLength 500 */
	path?: string;
	/** @maxLength 150 */
	user?: string;
	/**
	 * @format int64
	 * @min 0
	 * @max 9223372036854776000
	 */
	port?: number | null;
	/** @format date-time */
	submit_time?: string | null;
	/** @format date-time */
	start_time?: string | null;
	/** @format date-time */
	end_time?: string | null;
	/** @format date-time */
	error_time?: string | null;
	/**
	 * * `LOW` - LOW
	 * * `NORMAL` - NORMAL
	 * * `HIGH` - HIGH
	 */
	priority?: PriorityEnum;
	/**
	 * * `SLOW` - SLOW
	 * * `NORMAL` - NORMAL
	 * * `FAST` - FAST
	 * * `UNDEF` - UNDEF
	 */
	gpu_partition?: GpuPartitionEnum;
	/**
	 * @format int64
	 * @min 0
	 * @max 9223372036854776000
	 */
	duration?: number;
	/**
	 * * `PENDING` - PENDING
	 * * `FINISHED` - FINISHED
	 * * `INTERRUPTED` - INTERRUPTED
	 * * `RUNNING` - RUNNING
	 */
	status?: JobStatusEnum;
	output?: string | null;
	error?: string | null;
	/** @maxLength 150 */
	flags?: string | null;
	node?: number | null;
	gpu?: number | null;
}

/**
 * * `LOW` - LOW
 * * `NORMAL` - NORMAL
 * * `HIGH` - HIGH
 */
export enum PriorityEnum {
	LOW = 'LOW',
	NORMAL = 'NORMAL',
	HIGH = 'HIGH'
}

export interface RefreshNode {
	node_id?: number;
}

/**
 * * `SLOW` - SLOW
 * * `NORMAL` - NORMAL
 * * `FAST` - FAST
 */
export enum SpeedEnum {
	SLOW = 'SLOW',
	NORMAL = 'NORMAL',
	FAST = 'FAST'
}

export interface TokenObtainPair {
	username: string;
	password: string;
	readonly access: string;
	readonly refresh: string;
}

export interface TokenRefresh {
	readonly access: string;
	refresh: string;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, 'body' | 'bodyUsed'>;

export interface FullRequestParams extends Omit<RequestInit, 'body'> {
	/** set parameter to `true` for call `securityWorker` for this request */
	secure?: boolean;
	/** request path */
	path: string;
	/** content type of request body */
	type?: ContentType;
	/** query params */
	query?: QueryParamsType;
	/** format of response (i.e. response.json() -> format: "json") */
	format?: ResponseFormat;
	/** request body */
	body?: unknown;
	/** base url */
	baseUrl?: string;
	/** request cancellation token */
	cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, 'body' | 'method' | 'query' | 'path'>;

export interface ApiConfig<SecurityDataType = unknown> {
	baseUrl?: string;
	baseApiParams?: Omit<RequestParams, 'baseUrl' | 'cancelToken' | 'signal'>;
	securityWorker?: (
		securityData: SecurityDataType | null
	) => Promise<RequestParams | void> | RequestParams | void;
	customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
	data: D;
	error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
	Json = 'application/json',
	FormData = 'multipart/form-data',
	UrlEncoded = 'application/x-www-form-urlencoded',
	Text = 'text/plain'
}

export class HttpClient<SecurityDataType = unknown> {
	public baseUrl: string = '';
	private securityData: SecurityDataType | null = null;
	private securityWorker?: ApiConfig<SecurityDataType>['securityWorker'];
	private abortControllers = new Map<CancelToken, AbortController>();
	private customFetch = (...fetchParams: Parameters<typeof fetch>) => fetch(...fetchParams);

	private baseApiParams: RequestParams = {
		credentials: 'same-origin',
		headers: {},
		redirect: 'follow',
		referrerPolicy: 'no-referrer'
	};

	constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
		Object.assign(this, apiConfig);
	}

	public setSecurityData = (data: SecurityDataType | null) => {
		this.securityData = data;
	};

	protected encodeQueryParam(key: string, value: any) {
		const encodedKey = encodeURIComponent(key);
		return `${encodedKey}=${encodeURIComponent(typeof value === 'number' ? value : `${value}`)}`;
	}

	protected addQueryParam(query: QueryParamsType, key: string) {
		return this.encodeQueryParam(key, query[key]);
	}

	protected addArrayQueryParam(query: QueryParamsType, key: string) {
		const value = query[key];
		return value.map((v: any) => this.encodeQueryParam(key, v)).join('&');
	}

	protected toQueryString(rawQuery?: QueryParamsType): string {
		const query = rawQuery || {};
		const keys = Object.keys(query).filter((key) => 'undefined' !== typeof query[key]);
		return keys
			.map((key) =>
				Array.isArray(query[key])
					? this.addArrayQueryParam(query, key)
					: this.addQueryParam(query, key)
			)
			.join('&');
	}

	protected addQueryParams(rawQuery?: QueryParamsType): string {
		const queryString = this.toQueryString(rawQuery);
		return queryString ? `?${queryString}` : '';
	}

	private contentFormatters: Record<ContentType, (input: any) => any> = {
		[ContentType.Json]: (input: any) =>
			input !== null && (typeof input === 'object' || typeof input === 'string')
				? JSON.stringify(input)
				: input,
		[ContentType.Text]: (input: any) =>
			input !== null && typeof input !== 'string' ? JSON.stringify(input) : input,
		[ContentType.FormData]: (input: any) =>
			Object.keys(input || {}).reduce((formData, key) => {
				const property = input[key];
				formData.append(
					key,
					property instanceof Blob
						? property
						: typeof property === 'object' && property !== null
						? JSON.stringify(property)
						: `${property}`
				);
				return formData;
			}, new FormData()),
		[ContentType.UrlEncoded]: (input: any) => this.toQueryString(input)
	};

	protected mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
		return {
			...this.baseApiParams,
			...params1,
			...(params2 || {}),
			headers: {
				...(this.baseApiParams.headers || {}),
				...(params1.headers || {}),
				...((params2 && params2.headers) || {})
			}
		};
	}

	protected createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
		if (this.abortControllers.has(cancelToken)) {
			const abortController = this.abortControllers.get(cancelToken);
			if (abortController) {
				return abortController.signal;
			}
			return void 0;
		}

		const abortController = new AbortController();
		this.abortControllers.set(cancelToken, abortController);
		return abortController.signal;
	};

	public abortRequest = (cancelToken: CancelToken) => {
		const abortController = this.abortControllers.get(cancelToken);

		if (abortController) {
			abortController.abort();
			this.abortControllers.delete(cancelToken);
		}
	};

	public request = async <T = any, E = any>({
		body,
		secure,
		path,
		type,
		query,
		format,
		baseUrl,
		cancelToken,
		...params
	}: FullRequestParams): Promise<HttpResponse<T, E>> => {
		const secureParams =
			((typeof secure === 'boolean' ? secure : this.baseApiParams.secure) &&
				this.securityWorker &&
				(await this.securityWorker(this.securityData))) ||
			{};
		const requestParams = this.mergeRequestParams(params, secureParams);
		const queryString = query && this.toQueryString(query);
		const payloadFormatter = this.contentFormatters[type || ContentType.Json];
		const responseFormat = format || requestParams.format;

		return this.customFetch(
			`${baseUrl || this.baseUrl || ''}${path}${queryString ? `?${queryString}` : ''}`,
			{
				...requestParams,
				headers: {
					...(requestParams.headers || {}),
					...(type && type !== ContentType.FormData ? { 'Content-Type': type } : {})
				},
				signal: (cancelToken ? this.createAbortSignal(cancelToken) : requestParams.signal) || null,
				body: typeof body === 'undefined' || body === null ? null : payloadFormatter(body)
			}
		).then(async (response) => {
			const r = response as HttpResponse<T, E>;
			r.data = null as unknown as T;
			r.error = null as unknown as E;

			const data = !responseFormat
				? r
				: await response[responseFormat]()
						.then((data) => {
							if (r.ok) {
								r.data = data;
							} else {
								r.error = data;
							}
							return r;
						})
						.catch((e) => {
							r.error = e;
							return r;
						});

			if (cancelToken) {
				this.abortControllers.delete(cancelToken);
			}

			if (!response.ok) throw data;
			return data;
		});
	};
}

/**
 * @title No title
 * @version 0.0.0
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
	api = {
		/**
		 * No description
		 *
		 * @tags gpus
		 * @name GpusList
		 * @request GET:/api/gpus/
		 * @secure
		 */
		gpusList: (
			query?: {
				/** Number of results to return per page. */
				limit?: number;
				/** The initial index from which to return the results. */
				offset?: number;
			},
			params: RequestParams = {}
		) =>
			this.request<PaginatedGpuList, any>({
				path: `/api/gpus/`,
				method: 'GET',
				query: query,
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags gpus
		 * @name GpusCreate
		 * @request POST:/api/gpus/
		 * @secure
		 */
		gpusCreate: (data: Gpu, params: RequestParams = {}) =>
			this.request<Gpu, any>({
				path: `/api/gpus/`,
				method: 'POST',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags gpus
		 * @name GpusRetrieve
		 * @request GET:/api/gpus/{id}/
		 * @secure
		 */
		gpusRetrieve: (id: number, params: RequestParams = {}) =>
			this.request<Gpu, any>({
				path: `/api/gpus/${id}/`,
				method: 'GET',
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags gpus
		 * @name GpusDestroy
		 * @request DELETE:/api/gpus/{id}/
		 * @secure
		 */
		gpusDestroy: (id: number, params: RequestParams = {}) =>
			this.request<void, any>({
				path: `/api/gpus/${id}/`,
				method: 'DELETE',
				secure: true,
				...params
			}),

		/**
		 * No description
		 *
		 * @tags gpus
		 * @name GpusRefreshCreate
		 * @request POST:/api/gpus/{id}/refresh/
		 * @secure
		 */
		gpusRefreshCreate: (id: number, data: Gpu, params: RequestParams = {}) =>
			this.request<Gpu, any>({
				path: `/api/gpus/${id}/refresh/`,
				method: 'POST',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags jobs
		 * @name JobsList
		 * @request GET:/api/jobs/
		 * @secure
		 */
		jobsList: (
			query?: {
				gpu?: number;
				/** Number of results to return per page. */
				limit?: number;
				node?: number;
				/** The initial index from which to return the results. */
				offset?: number;
				/**
				 * * `LOW` - LOW
				 * * `NORMAL` - NORMAL
				 * * `HIGH` - HIGH
				 */
				priority?: 'HIGH' | 'LOW' | 'NORMAL';
				/**
				 * * `PENDING` - PENDING
				 * * `FINISHED` - FINISHED
				 * * `INTERRUPTED` - INTERRUPTED
				 * * `RUNNING` - RUNNING
				 */
				status?: 'FINISHED' | 'INTERRUPTED' | 'PENDING' | 'RUNNING';
				user?: string;
			},
			params: RequestParams = {}
		) =>
			this.request<PaginatedJobList, any>({
				path: `/api/jobs/`,
				method: 'GET',
				query: query,
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags jobs
		 * @name JobsCreate
		 * @request POST:/api/jobs/
		 * @secure
		 */
		jobsCreate: (data: Job, params: RequestParams = {}) =>
			this.request<Job, any>({
				path: `/api/jobs/`,
				method: 'POST',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags jobs
		 * @name JobsRetrieve
		 * @request GET:/api/jobs/{id}/
		 * @secure
		 */
		jobsRetrieve: (id: number, params: RequestParams = {}) =>
			this.request<Job, any>({
				path: `/api/jobs/${id}/`,
				method: 'GET',
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags jobs
		 * @name JobsUpdate
		 * @request PUT:/api/jobs/{id}/
		 * @secure
		 */
		jobsUpdate: (id: number, data: Job, params: RequestParams = {}) =>
			this.request<Job, any>({
				path: `/api/jobs/${id}/`,
				method: 'PUT',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags jobs
		 * @name JobsPartialUpdate
		 * @request PATCH:/api/jobs/{id}/
		 * @secure
		 */
		jobsPartialUpdate: (id: number, data: PatchedJob, params: RequestParams = {}) =>
			this.request<Job, any>({
				path: `/api/jobs/${id}/`,
				method: 'PATCH',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags jobs
		 * @name JobsDestroy
		 * @request DELETE:/api/jobs/{id}/
		 * @secure
		 */
		jobsDestroy: (id: number, params: RequestParams = {}) =>
			this.request<void, any>({
				path: `/api/jobs/${id}/`,
				method: 'DELETE',
				secure: true,
				...params
			}),

		/**
		 * No description
		 *
		 * @tags jobs
		 * @name JobsStartCreate
		 * @request POST:/api/jobs/{id}/start/
		 * @secure
		 */
		jobsStartCreate: (id: number, data: Job, params: RequestParams = {}) =>
			this.request<Job, any>({
				path: `/api/jobs/${id}/start/`,
				method: 'POST',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags nodes
		 * @name NodesList
		 * @request GET:/api/nodes/
		 * @secure
		 */
		nodesList: (
			query?: {
				/** Number of results to return per page. */
				limit?: number;
				/** The initial index from which to return the results. */
				offset?: number;
			},
			params: RequestParams = {}
		) =>
			this.request<PaginatedNodeList, any>({
				path: `/api/nodes/`,
				method: 'GET',
				query: query,
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags nodes
		 * @name NodesCreate
		 * @request POST:/api/nodes/
		 * @secure
		 */
		nodesCreate: (data: Node, params: RequestParams = {}) =>
			this.request<Node, any>({
				path: `/api/nodes/`,
				method: 'POST',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags nodes
		 * @name NodesRetrieve
		 * @request GET:/api/nodes/{id}/
		 * @secure
		 */
		nodesRetrieve: (id: number, params: RequestParams = {}) =>
			this.request<Node, any>({
				path: `/api/nodes/${id}/`,
				method: 'GET',
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags nodes
		 * @name NodesDestroy
		 * @request DELETE:/api/nodes/{id}/
		 * @secure
		 */
		nodesDestroy: (id: number, params: RequestParams = {}) =>
			this.request<void, any>({
				path: `/api/nodes/${id}/`,
				method: 'DELETE',
				secure: true,
				...params
			}),

		/**
		 * No description
		 *
		 * @tags nodes
		 * @name NodesRefreshCreate
		 * @request POST:/api/nodes/refresh/
		 * @secure
		 */
		nodesRefreshCreate: (data: RefreshNode, params: RequestParams = {}) =>
			this.request<RefreshNode, any>({
				path: `/api/nodes/refresh/`,
				method: 'POST',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * @description OpenApi3 schema for this API. Format can be selected via content negotiation. - YAML: application/vnd.oai.openapi - JSON: application/vnd.oai.openapi+json
		 *
		 * @tags schema
		 * @name SchemaRetrieve
		 * @request GET:/api/schema/
		 * @secure
		 */
		schemaRetrieve: (
			query?: {
				format?: 'json' | 'yaml';
				lang?:
					| 'af'
					| 'ar'
					| 'ar-dz'
					| 'ast'
					| 'az'
					| 'be'
					| 'bg'
					| 'bn'
					| 'br'
					| 'bs'
					| 'ca'
					| 'ckb'
					| 'cs'
					| 'cy'
					| 'da'
					| 'de'
					| 'dsb'
					| 'el'
					| 'en'
					| 'en-au'
					| 'en-gb'
					| 'eo'
					| 'es'
					| 'es-ar'
					| 'es-co'
					| 'es-mx'
					| 'es-ni'
					| 'es-ve'
					| 'et'
					| 'eu'
					| 'fa'
					| 'fi'
					| 'fr'
					| 'fy'
					| 'ga'
					| 'gd'
					| 'gl'
					| 'he'
					| 'hi'
					| 'hr'
					| 'hsb'
					| 'hu'
					| 'hy'
					| 'ia'
					| 'id'
					| 'ig'
					| 'io'
					| 'is'
					| 'it'
					| 'ja'
					| 'ka'
					| 'kab'
					| 'kk'
					| 'km'
					| 'kn'
					| 'ko'
					| 'ky'
					| 'lb'
					| 'lt'
					| 'lv'
					| 'mk'
					| 'ml'
					| 'mn'
					| 'mr'
					| 'ms'
					| 'my'
					| 'nb'
					| 'ne'
					| 'nl'
					| 'nn'
					| 'os'
					| 'pa'
					| 'pl'
					| 'pt'
					| 'pt-br'
					| 'ro'
					| 'ru'
					| 'sk'
					| 'sl'
					| 'sq'
					| 'sr'
					| 'sr-latn'
					| 'sv'
					| 'sw'
					| 'ta'
					| 'te'
					| 'tg'
					| 'th'
					| 'tk'
					| 'tr'
					| 'tt'
					| 'udm'
					| 'ug'
					| 'uk'
					| 'ur'
					| 'uz'
					| 'vi'
					| 'zh-hans'
					| 'zh-hant';
			},
			params: RequestParams = {}
		) =>
			this.request<Record<string, any>, any>({
				path: `/api/schema/`,
				method: 'GET',
				query: query,
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * @description Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.
		 *
		 * @tags token
		 * @name TokenCreate
		 * @request POST:/api/token/
		 */
		tokenCreate: (data: TokenObtainPair, params: RequestParams = {}) =>
			this.request<TokenObtainPair, any>({
				path: `/api/token/`,
				method: 'POST',
				body: data,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * @description Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.
		 *
		 * @tags token
		 * @name TokenRefreshCreate
		 * @request POST:/api/token/refresh/
		 */
		tokenRefreshCreate: (data: TokenRefresh, params: RequestParams = {}) =>
			this.request<TokenRefresh, any>({
				path: `/api/token/refresh/`,
				method: 'POST',
				body: data,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags users
		 * @name UsersList
		 * @request GET:/api/users/
		 * @secure
		 */
		usersList: (
			query?: {
				/** Number of results to return per page. */
				limit?: number;
				/** The initial index from which to return the results. */
				offset?: number;
			},
			params: RequestParams = {}
		) =>
			this.request<PaginatedCustomUserList, any>({
				path: `/api/users/`,
				method: 'GET',
				query: query,
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags users
		 * @name UsersCreate
		 * @request POST:/api/users/
		 * @secure
		 */
		usersCreate: (data: CustomUser, params: RequestParams = {}) =>
			this.request<CustomUser, any>({
				path: `/api/users/`,
				method: 'POST',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags users
		 * @name UsersRetrieve
		 * @request GET:/api/users/{id}/
		 * @secure
		 */
		usersRetrieve: (id: number, params: RequestParams = {}) =>
			this.request<CustomUser, any>({
				path: `/api/users/${id}/`,
				method: 'GET',
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags users
		 * @name UsersUpdate
		 * @request PUT:/api/users/{id}/
		 * @secure
		 */
		usersUpdate: (id: number, data: CustomUser, params: RequestParams = {}) =>
			this.request<CustomUser, any>({
				path: `/api/users/${id}/`,
				method: 'PUT',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags users
		 * @name UsersPartialUpdate
		 * @request PATCH:/api/users/{id}/
		 * @secure
		 */
		usersPartialUpdate: (id: number, data: PatchedCustomUser, params: RequestParams = {}) =>
			this.request<CustomUser, any>({
				path: `/api/users/${id}/`,
				method: 'PATCH',
				body: data,
				secure: true,
				type: ContentType.Json,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags users
		 * @name UsersDestroy
		 * @request DELETE:/api/users/{id}/
		 * @secure
		 */
		usersDestroy: (id: number, params: RequestParams = {}) =>
			this.request<void, any>({
				path: `/api/users/${id}/`,
				method: 'DELETE',
				secure: true,
				...params
			})
	};
}
