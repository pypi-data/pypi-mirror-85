/**
 * The type for a Snippet.
 * based on the implemented extension here
 * https://github.com/QuantStack/jupyterlab-snippets
 */
export declare type Snippet = string[];
/**
 * The Snippet Content interface
 */
export interface SnippetContent {
    content: string;
}
/**
 * List the available snippets.
 */
export declare function listSnippets(): Promise<Snippet[]>;
/**
 * Fetch a snippet given its path.
 * @param snippet The path of the snippet to fetch.
 */
export declare function fetchSnippet(snippet: Snippet): Promise<SnippetContent>;
