import operations_research as opr
import flexible_job_shop_data as fjsd


def main():
    data = fjsd.FlexibleShopJob()
    filename = ''
    data.load(filename)
    opr.FlexibleJobshop(data)


if __name__ == '__main__':
    main()
