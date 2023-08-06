import { PathExt } from "@jupyterlab/coreutils";
import { IMainMenu } from "@jupyterlab/mainmenu";
import { INotebookTracker, NotebookActions } from "@jupyterlab/notebook";
import { MenuSvg, pythonIcon, terminalIcon, textEditorIcon, folderIcon, } from '@jupyterlab/ui-components';
import { listSnippets, fetchSnippet } from "./snippets";
/**
 * The command IDs used by the snippets plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = "snippets:open";
})(CommandIDs || (CommandIDs = {}));
/**
 * Convert the list of snippets a tree.
 * @param snippets The list of snippets.
 */
function toTree(snippets) {
    const tree = new Map();
    snippets.forEach(snippet => {
        let node = tree;
        snippet.forEach(part => {
            if (!node.has(part)) {
                node.set(part, new Map());
            }
            node = node.get(part);
        });
    });
    return tree;
}
/**
 * Create a menu from a tree of snippets.
 * @param commands The command registry.
 * @param tree The tree of snippets.
 * @param path The current path in the tree.
 */
function createMenu(commands, tree, path = []) {
    const menu = new MenuSvg({ commands });
    for (const [name, map] of tree.entries()) {
        const fullpath = path.concat(name);
        if (map.size === 0) {
            menu.addItem({
                command: CommandIDs.open,
                args: { label: name, path: fullpath }
            });
        }
        else {
            const submenu = createMenu(commands, map, path.concat(name));
            submenu.title.label = name;
            submenu.title.icon = folderIcon;
            menu.addItem({ type: 'submenu', submenu });
        }
    }
    return menu;
}
/**
 * Initialization data for the jupyterlab-snippets extension.
 */
const extension = {
    id: "snippetlib_jl",
    autoStart: true,
    optional: [IMainMenu, INotebookTracker],
    activate: async (app, menu, notebookTracker) => {
        const { commands } = app;
        const isEnabled = () => {
            var _a, _b;
            return (((_a = notebookTracker) === null || _a === void 0 ? void 0 : _a.currentWidget) !== null &&
                ((_b = notebookTracker) === null || _b === void 0 ? void 0 : _b.currentWidget) === app.shell.currentWidget);
        };
        commands.addCommand(CommandIDs.open, {
            label: args => args['label'],
            icon: args => {
                const ext = PathExt.extname(args['label']);
                if (ext === '.py') {
                    return pythonIcon;
                }
                if (ext === '.sh') {
                    return terminalIcon;
                }
                return textEditorIcon;
            },
            execute: async (args) => {
                const path = args['path'];
                const response = await fetchSnippet(path);
                const content = response.content;
                if (!isEnabled()) {
                    return;
                }
                const current = notebookTracker.currentWidget;
                const notebook = current.content;
                NotebookActions.insertAbove(notebook);
                const activeCell = notebook.activeCell;
                activeCell.model.value.text = content;
            },
            isEnabled
        });
        if (menu) {
            const list = await listSnippets();
            const snippetsMenu = createMenu(commands, toTree(list));
            snippetsMenu.title.label = 'KD-Snippets';
            menu.addMenu(snippetsMenu);
        }
    }
};
export default extension;
