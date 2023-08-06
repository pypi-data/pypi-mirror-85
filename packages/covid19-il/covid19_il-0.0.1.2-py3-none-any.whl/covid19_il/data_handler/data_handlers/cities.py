from collections import namedtuple, defaultdict
from datetime import datetime as dt
from functools import lru_cache
from typing import Dict, NamedTuple, DefaultDict

from covid19_il.logger.logger import Logger
from covid19_il.data_handler.data_handlers.data_handler import DataHandler


class Cities(DataHandler):
    """ covid19_il Cities Data Handler.

    Attributes:
        None.

    Methods:
        cities_by_date(self, date: str = dt.strftime(dt.now(), format="%Y-%m-%d")): return calculated dictionary of
            city_name: namedtuple with city's data props via given date
        _get_top_cases_statistics(self, cities_fields: Tuple[AnyStr]): Helper Method of other class's method for
            calculation.
        top_cases_in_cities_by_date(self): returns top 10 cities with 5 calculated properties.
        cases_statistics(self): returns cases statistics.

    """

    fields = ("City_name", "City_code", "Date", "Cumulative_verified_cases", "Cumulated_recovered",
              "Cumulated_deaths", "Cumulated_number_of_tests", "Cumulated_number_of_diagnostic_tests")
    city = namedtuple("City", fields, defaults=(None,) * len(fields))

    def __init__(self, logger: Logger.logger, json_data: dict) -> None:
        """ Initialize Base Class & Instance Attributes """
        super().__init__(logger, json_data)
        self._logger.info(f"{self.__class__.__name__} Data Handler has been created.")

    @lru_cache(maxsize=None)
    def cities_by_date(self, date: str = dt.strftime(dt.now(), format="%Y-%m-%d")) -> DefaultDict[str, NamedTuple]:
        """ Return calculated dictionary of city_name: namedtuple with city's data props via given date in format
            like: '2020-10-03'.

        Args:
            date(str): date as a string.

        Returns:
            data_dict(dict or none): cities by date data stored in a dictionary.

        Raises:
            KeyError: concrete error which can occurred if data frame can't be access by given key.
        """

        self._logger.info(f"starting {self.__class__.__name__}'s {self.cities_by_date.__name__} method.")
        data_dict = None
        try:
            df = self._get_clean_copy_df_data()
            df = df[df["Date"] == date]
            data = df.groupby([*df.columns])["Date"].unique()
            data_dict = defaultdict(NamedTuple)

            for key in data.keys():
                data_dict[key[0]] = Cities.city(*key)

        except KeyError as ke:
            self._logger.exception(ke, "No DataFrame's key exists according to the api client's query results")
        finally:
            return data_dict

    def _get_top_cases_statistics(self,  date: str) -> DefaultDict[str, DefaultDict[str, int]]:
        """ Helper Method of top_cases_in_cities_by_date method for calculation.

        Note:
            private method which get called by top_cases_in_cities's method.
        Args:
            date(str): today's date as a string.

        Returns:
            data_dict(DefaultDict[str, DefaultDict[str, int]]): top cities statistics data holder.

        """

        data_dict = None
        try:
            df = self._get_clean_copy_df_data()
            df = df[df["Date"] == date]

            for column_name in Cities.fields[3:]:
                df[column_name] = [self._convert_string_to_int(item) for item in df[column_name]]

            data_dict = defaultdict(lambda: defaultdict(int))
            for field in Cities.fields[3:]:
                temp_df = df[["City_Name", field]]
                temp_df = temp_df.sort_values(field, ascending=False).head(10)
                for value in temp_df.values:
                    data_dict[field][value[0]] = value[1]

        except KeyError as ke:
            self._logger.exception(ke, "No DataFrame's key exists according to the api client's query results")
        finally:
            return data_dict

    @lru_cache
    def top_cases_in_cities_by_date(self, date: str = dt.strftime(dt.now(), format="%Y-%m-%d")) \
            -> DefaultDict[str, DefaultDict[str, int]]:
        """ Returns top 10 cities with 5 calculated properties.

        Args:
            date(str): date as a string..

        Returns:
            _(DefaultDict[str, DefaultDict[str, int]]): top cities statistics data holder.

        """

        return self._get_top_cases_statistics(date)

    @lru_cache
    def cases_statistics(self) -> Dict[str, Dict[str, int or float]]:
        """ Returns cases statistics.

        Note:
            use inherited methods from base class.
        Args:
            None.

        Returns:
            _(DefaultDict[str, DefaultDict[str, int]]): top cities statistics data holder.

        """

        return self._get_statistics_by_columns_names(Cities.fields[3:])
