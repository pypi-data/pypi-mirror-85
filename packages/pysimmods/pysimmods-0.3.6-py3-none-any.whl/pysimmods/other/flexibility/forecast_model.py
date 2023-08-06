"""This module contains the flexibility model."""
from datetime import datetime, timedelta

import numpy as np

import pandas as pd
from pysimmods.util.dateformat import GER


class ForecastModel:
    """The flexibility model for all pysimmods."""

    def __init__(
        self,
        model,
        start_date,
        step_size,
        forecast_horizon_hours=1,
        flexibility_horizon_hours=3,
        num_schedules=10,
        seed=None,
        unit="kw",
    ):
        self.model = model
        """A reference to the model"""

        if isinstance(start_date, str):
            self.now_dt = datetime.strptime(start_date, GER)
        else:
            self.now_dt = start_date
        """The current local time."""

        self.step_size = step_size
        """The step size of the model."""

        self.factor = 1.0
        self.pname = "p_kw"
        self.qname = "q_kvar"

        if unit == "mw":
            self.factor = 0.001
            self.pname = "p_mw"
            self.qname = "q_mvar"
        elif unit == "w":
            self.factor = 1000.0
            self.pname = "p_w"
            self.qname = "q_var"

        self.schedule = None
        """A dictionary containing the schedule for the model."""
        self.active_schedule_id = None
        """A pointer to the currently active schedule."""

        self.forecasts = None
        """A dictionary containing forecasts for the inputs of 
        the underlying model.
        """
        self.flexibilities = None
        """A dictionary containing the current flexibilities of
        the underlying model.
        """
        self.forecast_horizon_hours = forecast_horizon_hours
        self.num_schedules = num_schedules

        if seed is not None:
            self.rng = np.random.RandomState(seed)
        else:
            self.rng = np.random.RandomState()

    def update_forecasts(self, forecasts):
        if self.forecasts is None:
            self.forecasts = forecasts
        else:
            for col in forecasts.columns:
                if col not in self.forecasts.columns:
                    self.forecasts[col] = np.nan
            for index, _ in forecasts.iterrows():
                if index not in self.forecasts.index:
                    break

            self.forecasts.update(forecasts.loc[:index])
            self.forecasts = self.forecasts.append(forecasts.loc[index:])

            self.forecasts = self.forecasts[~self.forecasts.index.duplicated()]

    def update_schedule(self, schedule):
        if self.schedule is None:
            self._create_schedule_dataframe()

        for index, _ in schedule.iterrows():
            if index not in self.schedule.index:
                break

        self.schedule.update(schedule.loc[:index])
        self.schedule = self.schedule.append(schedule.loc[index:])

        self.schedule = self.schedule[~self.schedule.index.duplicated()]

        # self.schedule.update(schedule)

    def _create_schedule_dataframe(self):
        # periods = 1*3_600/self.step_size
        index = pd.date_range(
            self.now_dt,
            self.now_dt
            + timedelta(hours=1)
            - timedelta(seconds=self.step_size),
            freq="{}S".format(self.step_size),
        )
        self.schedule = pd.DataFrame(
            columns=["target", self.pname, self.qname], index=index
        )

    def _get_setpoint(self):

        if ~np.isnan(self.schedule.loc[self.now_dt]["target"]):
            setpoint = self.schedule.loc[self.now_dt]["target"] * 100
        else:
            try:
                setpoint = self.model.set_percent
            except TypeError:
                setpoint = None

        if setpoint is not None:
            self.schedule.loc[self.now_dt, "target"] = (
                setpoint * 0.01
            )  # FIXME: Remove the multiplier
            return setpoint

        setpoint = self.schedule.loc[self.now_dt]["target"] * 100

        return setpoint

    def step(self):
        """Perform a simulation step of the underlying model.

        Also updates the internal state of the flexibility model.

        """
        # Update the step size
        self.step_size = self.model.inputs.step_size
        self.model.inputs.now = self.now_dt

        if self.schedule is None:
            self._create_schedule_dataframe()

        setpoint = self._get_setpoint()
        if setpoint is not None and ~np.isnan(setpoint):
            self.model.set_percent = setpoint
        else:
            setpoint = 100.0

        self.model.step()

        self.schedule.loc[self.now_dt]["target"] = setpoint
        self.schedule.loc[self.now_dt.strftime(GER), self.pname] = (
            self.model.p_kw * self.factor
        )
        self.schedule.loc[self.now_dt.strftime(GER), self.qname] = (
            self.model.q_kvar * self.factor
        )

        self._check_schedule()
        self.now_dt += timedelta(seconds=self.step_size)

    def _check_schedule(self):

        now = self.now_dt + timedelta(seconds=self.step_size)
        limit = int(self.forecast_horizon_hours * 3_600 / self.step_size)
        reschedule = False

        for counter in range(limit):
            if now not in self.schedule.index:
                reschedule = True
                break
            elif np.isnan(self.schedule.loc[now]["target"]):
                reschedule = True
                break
            elif np.isnan(self.schedule.loc[now][self.pname]):
                reschedule = True
                break
            elif np.isnan(self.schedule.loc[now][self.qname]):
                reschedule = True
                break
            else:
                now += timedelta(seconds=self.step_size)

        if reschedule:
            self._create_init_schedule()
            self.schedule = self.schedule.loc[self.now_dt :]

    def _create_init_schedule(self):
        state_backup = self.model.get_state()

        now = self.now_dt + timedelta(seconds=self.step_size)
        periods = int(self.forecast_horizon_hours * 2 * 3_600 / self.step_size)

        for _ in range(periods):
            if now not in self.schedule.index:
                self.schedule.loc[now] = [np.nan, np.nan, np.nan]
            default_setpoint = self.model.default_schedule[now.hour]
            if np.isnan(self.schedule.loc[now]["target"]):
                self.schedule.loc[now]["target"] = default_setpoint

            try:
                self._perform_step(now, self.schedule.loc[now]["target"] * 100)
                self.schedule.loc[now][self.pname] = (
                    self.model.p_kw * self.factor
                )
                self.schedule.loc[now][self.qname] = (
                    self.model.q_kvar * self.factor
                )
            except KeyError:
                # Forecast is missing
                self.schedule.loc[now, self.pname] = np.nan
                self.schedule.loc[now, self.qname] = np.nan
                self.schedule.loc[now, "target"] = np.nan
            now += timedelta(seconds=self.step_size)

        self.model.set_state(state_backup)

    def _perform_step(self, index, set_percent):
        self.model.set_percent = set_percent

        if self.forecasts is not None:
            # print(self.model)
            for col in self.forecasts.columns:
                if hasattr(self.model.inputs, col):
                    setattr(
                        self.model.inputs, col, self.forecasts.loc[index, col]
                    )

        self.model.inputs.now = index
        self.model.inputs.step_size = self.step_size
        self.model.step()

    @property
    def inputs(self):
        return self.model.inputs

    @property
    def config(self):
        return self.model.config

    @property
    def state(self):
        return self.model.state

    @property
    def set_percent(self):
        return self.model.set_percent

    @set_percent.setter
    def set_percent(self, set_percent):
        self.model.set_percent = set_percent
