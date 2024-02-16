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

export interface Gpus {
	/**
	 * @format int64
	 * @min -9223372036854776000
	 * @max 9223372036854776000
	 */
	device_id: number;
	uuid: string;
}

export interface Job {
	id: number;
	/** @maxLength 100 */
	user?: string | null;
}

export interface MS {
	queue_watchdog?: boolean;
}

export interface Nodes {
	/** @maxLength 15 */
	ip: string;
	/** @maxLength 15 */
	name: string;
}

export interface PatchedJob {
	id?: number;
	/** @maxLength 100 */
	user?: string | null;
}

export interface PatchedMS {
	queue_watchdog?: boolean;
}

export interface PatchedNodes {
	/** @maxLength 15 */
	ip?: string;
	/** @maxLength 15 */
	name?: string;
}

export interface TokenObtainPair {
	username: string;
	password: string;
	access: string;
	refresh: string;
}

export interface TokenRefresh {
	access: string;
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
		gpusList: (params: RequestParams = {}) =>
			this.request<Gpus[], any>({
				path: `/api/gpus/`,
				method: 'GET',
				secure: true,
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
			this.request<Gpus, any>({
				path: `/api/gpus/${id}/`,
				method: 'GET',
				secure: true,
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
		jobsList: (params: RequestParams = {}) =>
			this.request<Job[], any>({
				path: `/api/jobs/`,
				method: 'GET',
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
		 * @tags manager-settings
		 * @name ManagerSettingsList
		 * @request GET:/api/manager-settings/
		 * @secure
		 */
		managerSettingsList: (params: RequestParams = {}) =>
			this.request<MS[], any>({
				path: `/api/manager-settings/`,
				method: 'GET',
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags manager-settings
		 * @name ManagerSettingsCreate
		 * @request POST:/api/manager-settings/
		 * @secure
		 */
		managerSettingsCreate: (data: MS, params: RequestParams = {}) =>
			this.request<MS, any>({
				path: `/api/manager-settings/`,
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
		 * @tags manager-settings
		 * @name ManagerSettingsRetrieve
		 * @request GET:/api/manager-settings/{id}/
		 * @secure
		 */
		managerSettingsRetrieve: (id: number, params: RequestParams = {}) =>
			this.request<MS, any>({
				path: `/api/manager-settings/${id}/`,
				method: 'GET',
				secure: true,
				format: 'json',
				...params
			}),

		/**
		 * No description
		 *
		 * @tags manager-settings
		 * @name ManagerSettingsUpdate
		 * @request PUT:/api/manager-settings/{id}/
		 * @secure
		 */
		managerSettingsUpdate: (id: number, data: MS, params: RequestParams = {}) =>
			this.request<MS, any>({
				path: `/api/manager-settings/${id}/`,
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
		 * @tags manager-settings
		 * @name ManagerSettingsPartialUpdate
		 * @request PATCH:/api/manager-settings/{id}/
		 * @secure
		 */
		managerSettingsPartialUpdate: (id: number, data: PatchedMS, params: RequestParams = {}) =>
			this.request<MS, any>({
				path: `/api/manager-settings/${id}/`,
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
		 * @tags manager-settings
		 * @name ManagerSettingsDestroy
		 * @request DELETE:/api/manager-settings/{id}/
		 * @secure
		 */
		managerSettingsDestroy: (id: number, params: RequestParams = {}) =>
			this.request<void, any>({
				path: `/api/manager-settings/${id}/`,
				method: 'DELETE',
				secure: true,
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
		nodesList: (params: RequestParams = {}) =>
			this.request<Nodes[], any>({
				path: `/api/nodes/`,
				method: 'GET',
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
		nodesCreate: (data: Nodes, params: RequestParams = {}) =>
			this.request<Nodes, any>({
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
			this.request<Nodes, any>({
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
		 * @name NodesUpdate
		 * @request PUT:/api/nodes/{id}/
		 * @secure
		 */
		nodesUpdate: (id: number, data: Nodes, params: RequestParams = {}) =>
			this.request<Nodes, any>({
				path: `/api/nodes/${id}/`,
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
		 * @tags nodes
		 * @name NodesPartialUpdate
		 * @request PATCH:/api/nodes/{id}/
		 * @secure
		 */
		nodesPartialUpdate: (id: number, data: PatchedNodes, params: RequestParams = {}) =>
			this.request<Nodes, any>({
				path: `/api/nodes/${id}/`,
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
			})
	};
}