import { RootState } from "@/store";
import { createSelector } from "@reduxjs/toolkit";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { Model } from "./type";

export const apiSlice = createApi({
  reducerPath: "model",
  baseQuery: fetchBaseQuery({ baseUrl: `http://localhost:3500` }),
  endpoints: (builder) => ({
    getModels: builder.query<Model[], void>({
      query: () => `/get-scripts`,
    }),
  }),
});

export const selectModelsResult = apiSlice.endpoints.getModels.select();

export const selectAllModels = createSelector(
  selectModelsResult,
  (modelResult) => (modelResult.data ? modelResult.data : [])
);

const modelNameSelector = createSelector(
  selectAllModels,
  (_: RootState, modelName: string) => modelName,
  (models, modelName) => models.find((model) => model.name === modelName)
);

export const selectModelByName = (modelName: string) => (state: RootState) =>
  modelNameSelector(state, modelName);

export const { useGetModelsQuery } = apiSlice;
