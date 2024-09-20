
export function paginate<T>(items: T[], page: number, perPage: number) {
  const offset = (page - 1) * perPage;
  const totalPages = Math.ceil(items.length / perPage);

  const paginatedItems = items.slice(offset, offset + perPage);

  return {
    previousPage: page - 1 ? page - 1 : null,
    nextPage: totalPages > page ? page + 1 : null,
    total: items.length,
    totalPages: totalPages,
    items: paginatedItems,
  };
}
