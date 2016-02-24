import { omit } from "lodash/object";
import { Resource } from "../../library";
import { compose } from "../../library/Selector"
import * as User from "../User";

const Module = new Resource("module", "id", {
    cleaner: mod => omit(mod, "papers")
});

/*
 * Get a paper by module, year and period.
 */
export const getModule = Module.createStatefulResourceAction(User.selectAPI, 
    (api, code) => api.getModule(code).then((resp) => resp["module"]));

/*
 * Search for modules.
 */
export const search = Module.createStatefulAction("MODULE_SEARCH", User.selectAPI, 
    (api, query) => api.searchModules(query));

/**
 * Select a module by code.
 * @param  {String}   code Module code.
 * @return {Function}      Selector.
 */
export const selectByCode = (code) => {
    return Module.select(modules => modules.find(mod => mod.code === code.toUpperCase()));
};

/**
 * Select a module by id.
 * @param  {String}   id   Module id.
 * @return {Function}      Selector.
 */
export const selectById = (id) => {
    return Module.select(modules => modules.find(mod => mod.id === id));
};

/**
 * Select papers for a module.
 * @param  {String}   code The module code.
 * @return {Function}      Selector.
 */
export const selectPapers = code => state => {
    return state.resources.papers.filter(paper => paper.module === code);
};

/**
 * Select a module by ID (or code) and include papers.
 * @param  {Number}   id Module id.
 * @return {Function}    Selector.
 */
export const selectByCodeWithPapers = compose(selectByCode, mod => state => ({ 
    ...module, 
    papers: selectPapers(mod.code)(state)
}));

/*
 * Enure modules loaded by user get store in modules resource.
 */
Module.addProducerHandler(User.getModules, ({ modules }) => modules);
Module.addProducerHandler(search, ({ modules }) => modules);

export default Module;