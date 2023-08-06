import { URLExt } from "@jupyterlab/coreutils";
import { ServerConnection } from "@jupyterlab/services";
/**
 * List the available snippets.
 */
export async function listSnippets() {
    return requestAPI("list");
}
/**
 * Fetch a snippet given its path.
 * @param snippet The path of the snippet to fetch.
 */
export async function fetchSnippet(snippet) {
    let request = {
        method: 'POST',
        body: JSON.stringify({ snippet })
    };
    return requestAPI("get", request);
}
/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = "", init = {}) {
    const settings = ServerConnection.makeSettings();
    const requestUrl = URLExt.join(settings.baseUrl, "snippets", endPoint);
    let response;
    try {
        response = await ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new ServerConnection.NetworkError(error);
    }
    const data = await response.json();
    if (!response.ok) {
        throw new ServerConnection.ResponseError(response, data.message);
    }
    return data;
}
