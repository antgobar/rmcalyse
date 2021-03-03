import dask.dataframe as dd

from .base_plugin import BasePlugin

class Orthonormaliser(BasePlugin, plugin_name='orthonormalise'):

    def process(self, df, meta, other_data):
        xyz_array = df[['x','y','z']].to_dask_array(lengths=True)
        answer = (meta.M @ xyz_array.T).T
        answer_df = dd.from_dask_array(answer)
        answer_df.columns = ['{}_{}'.format(self.name, x) for x in 'xyz']

        df = df.merge(answer_df, left_index=True, right_index=True)
        return df


    @staticmethod
    def lint(plugin_dict):
        pass


